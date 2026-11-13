from dataclasses import dataclass


@dataclass(frozen=True)
class SequenceChunk:
    start: int
    end: int
    sequence: str


def chunk_sequence(
    sequence: str,
    chunk_size: int,
    overlap: int = 0
) -> list[SequenceChunk]:
    """
    Divide a DNA sequence into manageable chunks.

    Overlap helps preserve sequence context at boundaries.
    """
    if not isinstance(sequence, str):
        raise TypeError("Sequence must be a string.")

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size."
        )

    sequence = sequence.upper()

    if not sequence:
        return []

    step = chunk_size - overlap
    chunks = []

    for start in range(0, len(sequence), step):
        end = min(start + chunk_size, len(sequence))

        chunks.append(
            SequenceChunk(
                start=start,
                end=end,
                sequence=sequence[start:end]
            )
        )

        if end == len(sequence):
            break

    return chunks
