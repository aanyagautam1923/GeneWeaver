import pytest

from app.sequence_metrics import (
    validate_sequence,
    calculate_gc_content,
    calculate_at_content,
    nucleotide_composition,
    calculate_sequence_metrics,
)


def test_validate_sequence():
    assert validate_sequence("atgc") == "ATGC"


def test_gc_content():
    assert calculate_gc_content("ATGC") == 50.0


def test_at_content():
    assert calculate_at_content("ATGC") == 50.0


def test_nucleotide_composition():
    result = nucleotide_composition("AATTGGCC")

    assert result == {
        "A": 2,
        "T": 2,
        "G": 2,
        "C": 2,
    }


def test_calculate_sequence_metrics():
    result = calculate_sequence_metrics("ATGC")

    assert result["sequence_length"] == 4
    assert result["gc_content"] == 50.0
    assert result["at_content"] == 50.0
    assert result["gc_at_ratio"] == 1.0


def test_invalid_sequence():
    with pytest.raises(ValueError):
        validate_sequence("ATGX")
