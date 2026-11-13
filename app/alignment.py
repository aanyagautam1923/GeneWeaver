from dataclasses import dataclass


@dataclass
class AlignmentResult:
    aligned_reference: str
    aligned_query: str
    score: int
    identity: float
    mismatches: int
    gaps: int


def needleman_wunsch(
    reference: str,
    query: str,
    match_score: int = 2,
    mismatch_score: int = -1,
    gap_score: int = -2
) -> AlignmentResult:
    """
    Perform global DNA sequence alignment using
    the Needleman-Wunsch dynamic programming algorithm.
    """
    if not isinstance(reference, str) or not isinstance(query, str):
        raise TypeError("DNA sequences must be strings.")

    reference = reference.upper()
    query = query.upper()

    if not reference or not query:
        raise ValueError("DNA sequences cannot be empty.")

    valid_bases = set("ACGTN")

    if set(reference) - valid_bases or set(query) - valid_bases:
        raise ValueError("Sequences contain invalid DNA bases.")

    rows = len(reference) + 1
    cols = len(query) + 1

    # Initialize scoring matrix
    matrix = [
        [0] * cols
        for _ in range(rows)
    ]

    # Initialize traceback matrix
    traceback = [
        [None] * cols
        for _ in range(rows)
    ]

    for i in range(1, rows):
        matrix[i][0] = i * gap_score
        traceback[i][0] = "UP"

    for j in range(1, cols):
        matrix[0][j] = j * gap_score
        traceback[0][j] = "LEFT"

    # Fill dynamic programming matrix
    for i in range(1, rows):
        for j in range(1, cols):

            diagonal = matrix[i - 1][j - 1] + (
                match_score
                if reference[i - 1] == query[j - 1]
                else mismatch_score
            )

            up = matrix[i - 1][j] + gap_score
            left = matrix[i][j - 1] + gap_score

            best = max(diagonal, up, left)
            matrix[i][j] = best

            if best == diagonal:
                traceback[i][j] = "DIAGONAL"
            elif best == up:
                traceback[i][j] = "UP"
            else:
                traceback[i][j] = "LEFT"

    # Traceback
    aligned_reference = []
    aligned_query = []

    i = len(reference)
    j = len(query)

    while i > 0 or j > 0:

        direction = traceback[i][j]

        if direction == "DIAGONAL":
            aligned_reference.append(reference[i - 1])
            aligned_query.append(query[j - 1])
            i -= 1
            j -= 1

        elif direction == "UP":
            aligned_reference.append(reference[i - 1])
            aligned_query.append("-")
            i -= 1

        elif direction == "LEFT":
            aligned_reference.append("-")
            aligned_query.append(query[j - 1])
            j -= 1

    aligned_reference.reverse()
    aligned_query.reverse()

    ref_result = "".join(aligned_reference)
    query_result = "".join(aligned_query)

    matches = sum(
        a == b and a != "-"
        for a, b in zip(ref_result, query_result)
    )

    mismatches = sum(
        a != b and a != "-" and b != "-"
        for a, b in zip(ref_result, query_result)
    )

    gaps = sum(
        a == "-" or b == "-"
        for a, b in zip(ref_result, query_result)
    )

    identity = (matches / len(ref_result)) * 100

    return AlignmentResult(
        aligned_reference=ref_result,
        aligned_query=query_result,
        score=matrix[-1][-1],
        identity=identity,
        mismatches=mismatches,
        gaps=gaps
    )
