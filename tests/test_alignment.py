import pytest
from app.alignment import needleman_wunsch


def test_identical_sequences():
    result = needleman_wunsch("ATGC", "ATGC")

    assert result.score == 8
    assert result.identity == 100.0
    assert result.mismatches == 0
    assert result.gaps == 0


def test_different_sequences():
    result = needleman_wunsch("AAAA", "TTTT")

    assert result.mismatches == 4
    assert result.gaps == 0
    assert result.identity == 0.0


def test_alignment_contains_gaps():
    result = needleman_wunsch("ATGC", "ATGGC")

    assert "-" in result.aligned_reference or "-" in result.aligned_query
    assert len(result.aligned_reference) == len(result.aligned_query)


def test_empty_sequence():
    with pytest.raises(ValueError):
        needleman_wunsch("", "ATGC")


def test_invalid_dna():
    with pytest.raises(ValueError):
        needleman_wunsch("ATGX", "ATGC")


def test_case_insensitive_alignment():
    result = needleman_wunsch("atgc", "ATGC")

    assert result.identity == 100.0
