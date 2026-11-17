"""Batch DNA alignment with optional CUDA acceleration."""

import numpy as np

from app.cuda_utils import check_cuda_availability


DEFAULT_MATCH = 2
DEFAULT_MISMATCH = -1
DEFAULT_GAP = -2


def _cpu_alignment_score(
    sequence_a,
    sequence_b,
    match_score=DEFAULT_MATCH,
    mismatch_penalty=DEFAULT_MISMATCH,
    gap_penalty=DEFAULT_GAP,
):
    """Calculate global alignment score using Needleman-Wunsch."""

    rows = len(sequence_a) + 1
    cols = len(sequence_b) + 1

    dp = np.zeros((rows, cols), dtype=np.int32)

    for i in range(rows):
        dp[i, 0] = i * gap_penalty

    for j in range(cols):
        dp[0, j] = j * gap_penalty

    for i in range(1, rows):
        for j in range(1, cols):
            if sequence_a[i - 1] == sequence_b[j - 1]:
                diagonal = dp[i - 1, j - 1] + match_score
            else:
                diagonal = dp[i - 1, j - 1] + mismatch_penalty

            deletion = dp[i - 1, j] + gap_penalty
            insertion = dp[i, j - 1] + gap_penalty

            dp[i, j] = max(diagonal, deletion, insertion)

    return int(dp[-1, -1])


def _gpu_alignment_kernel():
    """Create the CUDA kernel only when Numba CUDA is available."""

    from numba import cuda

    @cuda.jit
    def kernel(a, b, lengths_a, lengths_b, scores, matrices,
               match_score, mismatch_penalty, gap_penalty):
        idx = cuda.grid(1)

        if idx >= scores.size:
            return

        len_a = lengths_a[idx]
        len_b = lengths_b[idx]
        width = len_b + 1

        for i in range(len_a + 1):
            matrices[idx, i, 0] = i * gap_penalty

        for j in range(len_b + 1):
            matrices[idx, 0, j] = j * gap_penalty

        for i in range(1, len_a + 1):
            for j in range(1, len_b + 1):

                if a[idx, i - 1] == b[idx, j - 1]:
                    diagonal = (
                        matrices[idx, i - 1, j - 1] + match_score
                    )
                else:
                    diagonal = (
                        matrices[idx, i - 1, j - 1] + mismatch_penalty
                    )

                deletion = matrices[idx, i - 1, j] + gap_penalty
                insertion = matrices[idx, i, j - 1] + gap_penalty

                best = max(diagonal, deletion, insertion)
                matrices[idx, i, j] = best

        scores[idx] = matrices[idx, len_a, len_b]

    return kernel


def align_batch(
    sequence_pairs,
    match_score=DEFAULT_MATCH,
    mismatch_penalty=DEFAULT_MISMATCH,
    gap_penalty=DEFAULT_GAP,
    use_gpu=True,
):
    """
    Align multiple DNA sequence pairs.

    Returns:
        Dictionary containing scores, processing mode and alignment count.
    """

    pairs = list(sequence_pairs)

    for pair in pairs:
        if len(pair) != 2:
            raise ValueError("Each item must contain exactly two sequences.")

        for sequence in pair:
            if not isinstance(sequence, str):
                raise TypeError("DNA sequences must be strings.")

            if any(base not in "ATGCN" for base in sequence.upper()):
                raise ValueError("Sequences may contain only A, T, G, C and N.")

    if not pairs:
        return {
            "scores": [],
            "processing_mode": "CPU",
            "alignment_count": 0,
        }

    pairs = [(a.upper(), b.upper()) for a, b in pairs]

    cuda_info = check_cuda_availability()

    if use_gpu and cuda_info.get("available"):
        try:
            from numba import cuda

            max_a = max(len(a) for a, _ in pairs)
            max_b = max(len(b) for _, b in pairs)
            count = len(pairs)

            a_array = np.zeros((count, max_a), dtype=np.uint8)
            b_array = np.zeros((count, max_b), dtype=np.uint8)

            lengths_a = np.zeros(count, dtype=np.int32)
            lengths_b = np.zeros(count, dtype=np.int32)

            for i, (a, b) in enumerate(pairs):
                encoded_a = np.frombuffer(a.encode("ascii"), dtype=np.uint8)
                encoded_b = np.frombuffer(b.encode("ascii"), dtype=np.uint8)

                a_array[i, :len(a)] = encoded_a
                b_array[i, :len(b)] = encoded_b

                lengths_a[i] = len(a)
                lengths_b[i] = len(b)

            scores = np.zeros(count, dtype=np.int32)

            matrices = np.zeros(
                (count, max_a + 1, max_b + 1),
                dtype=np.int32,
            )

            kernel = _gpu_alignment_kernel()

            threads = 128
            blocks = (count + threads - 1) // threads

            kernel[blocks, threads](
                cuda.to_device(a_array),
                cuda.to_device(b_array),
                cuda.to_device(lengths_a),
                cuda.to_device(lengths_b),
                cuda.to_device(scores),
                cuda.to_device(matrices),
                match_score,
                mismatch_penalty,
                gap_penalty,
            )

            # Retrieve scores from the GPU.
            device_scores = cuda.to_device(scores)
            kernel[blocks, threads](
                cuda.to_device(a_array),
                cuda.to_device(b_array),
                cuda.to_device(lengths_a),
                cuda.to_device(lengths_b),
                device_scores,
                cuda.to_device(matrices),
                match_score,
                mismatch_penalty,
                gap_penalty,
            )

            return {
                "scores": device_scores.copy_to_host().tolist(),
                "processing_mode": "GPU",
                "alignment_count": count,
            }

        except Exception:
            # Safely fall back to CPU if GPU execution fails.
            pass

    scores = [
        _cpu_alignment_score(
            a,
            b,
            match_score,
            mismatch_penalty,
            gap_penalty,
        )
        for a, b in pairs
    ]

    return {
        "scores": scores,
        "processing_mode": "CPU",
        "alignment_count": len(pairs),
    }


def align_pair(sequence_a, sequence_b, **kwargs):
    """Align one pair of DNA sequences."""

    result = align_batch([(sequence_a, sequence_b)], **kwargs)

    return {
        "score": result["scores"][0],
        "processing_mode": result["processing_mode"],
    }
