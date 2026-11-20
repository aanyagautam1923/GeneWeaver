from app.cuda_alignment import align_pair


def test_align_identical_sequences():
    result = align_pair("ATGC", "ATGC")

    assert isinstance(result, dict)
    assert result["score"] == 8


def test_align_different_sequences():
    result = align_pair("ATGC", "ATCC")

    assert isinstance(result, dict)
    assert isinstance(result["score"], (int, float))


def test_alignment_processing_mode():
    result = align_pair("ATGC", "ATGC")

    assert result["processing_mode"] in ("CPU", "CUDA", "GPU")
