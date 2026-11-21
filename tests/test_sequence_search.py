import pytest

from app.sequence_search import (
    validate_dna,
    reverse_complement,
    search_sequence,
)


def test_validate_dna():
    assert validate_dna("ATGC") == "ATGC"


def test_validate_dna_lowercase():
    assert validate_dna("atgc") == "ATGC"


def test_reverse_complement():
    assert reverse_complement("ATGC") == "GCAT"


def test_search_sequence_found():
    result = search_sequence("ATGCGATATCG", "GAT")

    assert result is not None
    assert len(result) > 0


def test_search_sequence_not_found():
    result = search_sequence("AAAAAA", "GGGG")

    assert result is not None
    assert len(result) == 0


def test_invalid_dna():
    with pytest.raises(ValueError):
        validate_dna("ATGX")
