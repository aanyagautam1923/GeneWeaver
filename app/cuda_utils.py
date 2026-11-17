def check_cuda_availability() -> dict:
    """
    Detect CUDA availability using Numba.

    Returns actual hardware status.
    Falls back safely when CUDA is unavailable.
    """

    try:
        from numba import cuda

        if not cuda.is_available():
            return {
                "available": False,
                "device_name": None,
                "compute_capability": None,
                "message": "CUDA is not available. CPU mode will be used."
            }

        device = cuda.get_current_device()

        return {
            "available": True,
            "device_name": device.name.decode()
            if isinstance(device.name, bytes)
            else str(device.name),
            "compute_capability": tuple(device.compute_capability),
            "message": "CUDA GPU detected successfully."
        }

    except ImportError:
        return {
            "available": False,
            "device_name": None,
            "compute_capability": None,
            "message": "Numba is not installed."
        }

    except Exception as error:
        return {
            "available": False,
            "device_name": None,
            "compute_capability": None,
            "message": f"CUDA detection failed: {error}"
        }


def is_cuda_available() -> bool:
    """Return True only when CUDA is available."""
    return check_cuda_availability()["available"]


def get_gpu_info() -> dict:
    """Return GPU information including memory when available."""

    status = check_cuda_availability()

    if not status["available"]:
        return {
            **status,
            "total_memory_mb": None,
            "free_memory_mb": None
        }

    try:
        from numba import cuda

        free_memory, total_memory = cuda.current_context().get_memory_info()

        return {
            **status,
            "total_memory_mb": round(total_memory / (1024 ** 2), 2),
            "free_memory_mb": round(free_memory / (1024 ** 2), 2)
        }

    except Exception as error:
        return {
            **status,
            "total_memory_mb": None,
            "free_memory_mb": None,
            "memory_error": str(error)
        }


def get_processing_mode() -> str:
    """Select the available processing mode."""
    return "GPU" if is_cuda_available() else "CPU"
