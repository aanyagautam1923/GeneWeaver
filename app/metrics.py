"""Central metrics interface for GeneWeaver."""

from app.sequence_metrics import (
    validate_sequence,
    calculate_gc_content,
    calculate_at_content,
    nucleotide_composition,
    calculate_sequence_metrics,
)
from app.melting_temperature import calculate_melting_temperature


def calculate_all_metrics(sequence: str) -> dict:
    """Calculate sequence composition and melting temperature."""

    sequence = validate_sequence(sequence)

    metrics = calculate_sequence_metrics(sequence)
    metrics["melting_temperature"] = calculate_melting_temperature(sequence)

    return metrics


def get_basic_metrics(sequence: str) -> dict:
    """Return basic DNA sequence statistics."""

    sequence = validate_sequence(sequence)

    return {
        "sequence_length": len(sequence),
        "gc_content": calculate_gc_content(sequence),
        "at_content": calculate_at_content(sequence),
        "nucleotide_composition": nucleotide_composition(sequence),
    }


__all__ = [
    "validate_sequence",
    "calculate_gc_content",
    "calculate_at_content",
    "nucleotide_composition",
    "calculate_sequence_metrics",
    "calculate_melting_temperature",
    "calculate_all_metrics",
    "get_basic_metrics",
]
