from app.cuda_utils import (
    check_cuda_availability,
    is_cuda_available,
    get_gpu_info,
    get_processing_mode,
)


def test_cuda_availability():
    result = check_cuda_availability()

    assert isinstance(result, dict)
    assert "available" in result


def test_is_cuda_available():
    result = is_cuda_available()

    assert isinstance(result, bool)


def test_gpu_info():
    result = get_gpu_info()

    assert isinstance(result, dict)
    assert "available" in result


def test_processing_mode():
    result = get_processing_mode()

    assert isinstance(result, str)
    assert result in ("CPU", "CUDA", "GPU")
