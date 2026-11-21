import pytest

from app.alignment import needleman_wunsch


def test_identical_sequences():
    result = needleman_wunsch("ATGC", "ATGC")
    assert result is not None


def test_alignment_result_exists():
    result = needleman_wunsch("ATGC", "ATCC")
    assert result is not None


def test_alignment_score():
    result = needleman_wunsch("ATGC", "ATGC")
    assert result.score > 0


def test_alignment_sequences_same_length():
    result = needleman_wunsch("ATGC", "ATCC")
    assert len(result.aligned_reference) == len(result.aligned_query)


def test_alignment_contains_valid_bases():
    result = needleman_wunsch("ATGC", "ATCC")
    allowed = set("ATGC-")
    assert set(result.aligned_reference).issubset(allowed)
    assert set(result.aligned_query).issubset(allowed)


def test_alignment_identity():
    result = needleman_wunsch("ATGC", "ATCC")
    assert result.identity == 75.0
    assert result.mismatches == 1


def test_invalid_input():
    with pytest.raises(ValueError):
        needleman_wunsch("ATGX", "ATGC")
