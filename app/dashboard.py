"""Dashboard data and system status for GeneWeaver."""

from app.metrics import calculate_all_metrics
from app.config import get_project_info
from app.cuda_utils import get_gpu_info, get_processing_mode


def get_dashboard_overview() -> dict:
    """Return project overview and processing information."""

    project = get_project_info()
    gpu_info = get_gpu_info()

    return {
        "project": project,
        "processing_mode": get_processing_mode(),
        "gpu": gpu_info,
        "status": "running",
    }


def analyze_dashboard_sequence(sequence: str) -> dict:
    """Analyze a DNA sequence and prepare dashboard statistics."""

    metrics = calculate_all_metrics(sequence)

    return {
        "success": True,
        "metrics": metrics,
    }


def get_dashboard_stats(sequence: str | None = None) -> dict:
    """Return dashboard statistics."""

    stats = {
        "project_name": "GeneWeaver",
        "processing_mode": get_processing_mode(),
    }

    if sequence:
        stats["sequence_metrics"] = calculate_all_metrics(sequence)

    return stats


def get_system_status() -> dict:
    """Return current CPU/GPU processing status."""

    gpu_info = get_gpu_info()
    processing_mode = get_processing_mode()

    return {
        "status": "online",
        "processing_mode": processing_mode,
        "gpu_available": gpu_info.get("available", False),
        "gpu_info": gpu_info,
    }


__all__ = [
    "get_dashboard_overview",
    "analyze_dashboard_sequence",
    "get_dashboard_stats",
    "get_system_status",
]
