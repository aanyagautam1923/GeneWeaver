"""API routes for GeneWeaver."""

from dataclasses import asdict, is_dataclass

from fastapi import APIRouter, HTTPException

from app.api.schemas import (
    SequenceAnalyzeRequest,
    AlignmentRequest,
    PAMDetectionRequest,
)
from app.metrics import calculate_all_metrics
from app.alignment import needleman_wunsch
from app.pam_detection import detect_pam_sites
from app.dashboard import get_system_status
from app.config import get_project_info


router = APIRouter()


def serialize_result(result):
    """Convert dataclass results into dictionaries."""

    if is_dataclass(result):
        return asdict(result)

    if hasattr(result, "to_dict"):
        return result.to_dict()

    if isinstance(result, (dict, list, str, int, float, bool)):
        return result

    return {"result": str(result)}


@router.get("/health")
def health_check():
    """Check API health."""

    project = get_project_info()

    return {
        "status": "healthy",
        "project": project["name"],
        "version": project["version"],
    }


@router.post("/sequence/analyze")
def analyze_sequence(request: SequenceAnalyzeRequest):
    """Analyze DNA sequence and calculate its metrics."""

    try:
        result = calculate_all_metrics(request.sequence)

        return {
            "success": True,
            "message": "Sequence analysis completed.",
            "data": result,
        }

    except (ValueError, TypeError) as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.post("/alignment")
def perform_alignment(request: AlignmentRequest):
    """Perform Needleman-Wunsch global alignment."""

    try:
        result = needleman_wunsch(
            request.sequence_a,
            request.sequence_b,
        )

        return {
            "success": True,
            "message": "Alignment completed.",
            "data": serialize_result(result),
        }

    except (ValueError, TypeError) as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.post("/pam/detect")
def detect_pam(request: PAMDetectionRequest):
    """Detect PAM sites in a DNA sequence."""

    try:
        result = detect_pam_sites(
            request.sequence,
            pam_pattern=request.pam_pattern,
            guide_length=request.guide_length,
        )

        return {
            "success": True,
            "message": "PAM detection completed.",
            "data": serialize_result(result),
        }

    except (ValueError, TypeError) as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/system/status")
def system_status():
    """Return CPU and GPU processing status."""

    return {
        "success": True,
        "data": get_system_status(),
    }


