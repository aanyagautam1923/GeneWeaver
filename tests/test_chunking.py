from app.chunking import chunk_sequence


def test_chunk_sequence_returns_chunks():
    result = chunk_sequence("ATGCATGCATGC", chunk_size=4, overlap=0)
    assert len(result) > 0


def test_chunk_sequence_chunk_size():
    result = chunk_sequence("ATGCATGCATGC", chunk_size=4, overlap=0)
    for chunk in result:
        assert len(chunk.sequence) <= 4


def test_chunk_sequence_overlap():
    result = chunk_sequence("ATGCATGCATGC", chunk_size=4, overlap=2)
    assert len(result) >= 3


def test_chunk_sequence_empty():
    result = chunk_sequence("", chunk_size=4, overlap=0)
    assert result == []
