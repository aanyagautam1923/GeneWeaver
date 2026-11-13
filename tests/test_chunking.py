import pytest
from app.chunking import chunk_sequence


def test_basic_chunking():
    chunks = chunk_sequence("ATGCGTAC", 4)

    assert [chunk.sequence for chunk in chunks] == [
        "ATGC", "GTAC"
    ]


def test_chunking_with_overlap():
    chunks = chunk_sequence("ATGCGTAC", 4, 2)

    assert [chunk.sequence for chunk in chunks] == [
        "ATGC", "GCGT", "GTAC"
    ]


def test_empty_sequence():
    assert chunk_sequence("", 4) == []


def test_invalid_chunk_size():
    with pytest.raises(ValueError):
        chunk_sequence("ATGC", 0)


def test_invalid_overlap():
    with pytest.raises(ValueError):
        chunk_sequence("ATGC", 4, 4)


def test_chunk_positions():
    chunks = chunk_sequence("ATGCGTAC", 4, 2)

    assert chunks[0].start == 0
    assert chunks[0].end == 4
    assert chunks[1].start == 2
