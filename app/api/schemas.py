"""Pydantic request and response schemas for GeneWeaver API."""

from pydantic import BaseModel, Field
from typing import Any


class SequenceAnalyzeRequest(BaseModel):
    """Request model for DNA sequence analysis."""

    sequence: str = Field(..., min_length=1, description="DNA sequence")


class AlignmentRequest(BaseModel):
    """Request model for pairwise DNA alignment."""

    sequence_a: str = Field(..., min_length=1)
    sequence_b: str = Field(..., min_length=1)


class PAMDetectionRequest(BaseModel):
    """Request model for PAM site detection."""

    sequence: str = Field(..., min_length=1)
    pam_pattern: str = "NGG"
    guide_length: int = Field(default=20, ge=1)


class SequenceMetricsResponse(BaseModel):
    """Response model for sequence statistics."""

    sequence_length: int
    gc_content: float
    at_content: float
    gc_at_ratio: float | None = None
    nucleotide_composition: dict[str, int]
    melting_temperature: float | None = None


class APIResponse(BaseModel):
    """General API response."""

    success: bool
    message: str = ""
    data: dict[str, Any] = Field(default_factory=dict)


class HealthResponse(BaseModel):
    """API health status."""

    status: str
    project: str = "GeneWeaver"
    version: str = "1.0.0"


__all__ = [
    "SequenceAnalyzeRequest",
    "AlignmentRequest",
    "PAMDetectionRequest",
    "SequenceMetricsResponse",
    "APIResponse",
    "HealthResponse",
]
