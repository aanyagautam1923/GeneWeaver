"""DNA sequence statistics utilities."""

from collections import Counter

DNA_BASES = ("A", "T", "G", "C")


def calculate_sequence_stats(sequence: str) -> dict:
    """Calculate basic DNA nucleotide statistics."""
    cleaned = "".join(sequence.split()).upper()
    length = len(cleaned)

    counts = Counter(cleaned)
    gc_count = counts["G"] + counts["C"]
    at_count = counts["A"] + counts["T"]

    return {
        "length": length,
        "A": counts["A"],
        "T": counts["T"],
        "G": counts["G"],
        "C": counts["C"],
        "GC_content": round((gc_count / length) * 100, 2) if length else 0.0,
        "AT_content": round((at_count / length) * 100, 2) if length else 0.0,
    }
