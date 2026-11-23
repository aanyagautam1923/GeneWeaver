from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.core.dna_engine import sequence_stats, reverse_complement, parse_fasta, needleman_wunsch, detect_pam
from app.core.performance_engine import fast_search, benchmark_search, system_metrics

router = APIRouter(prefix="/api/week2", tags=["Week 2 Engine"])

class SequenceRequest(BaseModel):
    sequence: str = Field(min_length=1)

class SearchRequest(BaseModel):
    sequence: str = Field(min_length=1)
    pattern: str = Field(min_length=1)

class AlignmentRequest(BaseModel):
    sequence1: str = Field(min_length=1)
    sequence2: str = Field(min_length=1)

class FastaRequest(BaseModel):
    fasta: str = Field(min_length=1)

@router.post("/analyze")
def analyze(req: SequenceRequest):
    try:
        return {"stats": sequence_stats(req.sequence), "reverse_complement": reverse_complement(req.sequence)}
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.post("/search")
def search(req: SearchRequest):
    try:
        positions = fast_search(req.sequence, req.pattern)
        return {"pattern": req.pattern, "positions": positions, "count": len(positions)}
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.post("/alignment")
def alignment(req: AlignmentRequest):
    try:
        return needleman_wunsch(req.sequence1, req.sequence2)
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.post("/fasta")
def fasta(req: FastaRequest):
    try:
        return {"records": parse_fasta(req.fasta)}
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.post("/pam")
def pam(req: SequenceRequest):
    try:
        hits = detect_pam(req.sequence)
        return {"hits": hits, "count": len(hits)}
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.post("/benchmark")
def benchmark(req: SearchRequest):
    try:
        return benchmark_search(req.sequence, req.pattern)
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/system")
def system():
    return system_metrics()
