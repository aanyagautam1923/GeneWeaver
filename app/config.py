import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROJECT_NAME = "GeneWeaver"
PROJECT_VERSION = "1.0.0"

DATA_DIR = PROJECT_ROOT / "data"
REFERENCE_DB_DIR = DATA_DIR / "reference_db"

OUTPUT_DIR = PROJECT_ROOT / "outputs"
REPORTS_DIR = PROJECT_ROOT / "reports"
LOGS_DIR = PROJECT_ROOT / "logs"

DEFAULT_MATCH_SCORE = 2
DEFAULT_MISMATCH_PENALTY = -1
DEFAULT_GAP_PENALTY = -2

DEFAULT_ALIGNMENT_ALGORITHM = "needleman_wunsch"

MAX_SEQUENCE_LENGTH = int(
    os.getenv("GENEWEAVER_MAX_SEQUENCE_LENGTH", "100000")
)

SUPPORTED_BASES = {"A", "T", "G", "C", "N"}

DEFAULT_PAM_PATTERN = "NGG"


def get_project_info() -> dict:
    """Return project information."""

    return {
        "name": PROJECT_NAME,
        "version": PROJECT_VERSION,
        "root": str(PROJECT_ROOT),
        "data_directory": str(DATA_DIR),
        "output_directory": str(OUTPUT_DIR),
        "reports_directory": str(REPORTS_DIR)
    }


def create_required_directories() -> None:
    """Create required project directories."""

    directories = [
        DATA_DIR,
        REFERENCE_DB_DIR,
        OUTPUT_DIR,
        REPORTS_DIR,
        LOGS_DIR
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
