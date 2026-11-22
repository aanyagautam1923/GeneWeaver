from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.sequence_search import search_sequence

router = APIRouter(
    prefix="/search",
    tags=["Sequence Search"],
)


class SequenceSearchRequest(BaseModel):
    reference: str = Field(..., min_length=1)
    query: str = Field(..., min_length=1)
    max_mismatches: int = Field(default=0, ge=0)
    both_strands: bool = True


@router.post("/")
def search_dna(request: SequenceSearchRequest):
    try:
        results = search_sequence(
            reference=request.reference,
            query=request.query,
            max_mismatches=request.max_mismatches,
            both_strands=request.both_strands,
        )

        return {
            "success": True,
            "message": "Sequence search completed successfully.",
            "data": {
                "reference_length": len(request.reference),
                "query_length": len(request.query),
                "total_matches": len(results),
                "results": results,
            },
        }

    except (ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc