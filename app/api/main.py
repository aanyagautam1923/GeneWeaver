"""FastAPI application entry point for GeneWeaver."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import PROJECT_NAME, PROJECT_VERSION, create_required_directories


create_required_directories()

app = FastAPI(
    title=PROJECT_NAME,
    version=PROJECT_VERSION,
    description=(
        "GeneWeaver is an educational DNA sequence analysis "
        "and CRISPR off-target detection platform."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    """Return API welcome information."""

    return {
        "project": PROJECT_NAME,
        "version": PROJECT_VERSION,
        "message": "Welcome to GeneWeaver API.",
        "documentation": "/docs",
        "health": "/health",
    }
