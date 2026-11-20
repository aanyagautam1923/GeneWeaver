"""Alignment heatmap generation for GeneWeaver."""

from pathlib import Path

from app.config import OUTPUT_DIR


def create_alignment_matrix(aligned_sequence_a: str, aligned_sequence_b: str) -> list:
    """Create a numerical matrix representing alignment matches and mismatches."""

    if not isinstance(aligned_sequence_a, str) or not isinstance(aligned_sequence_b, str):
        raise TypeError("Aligned sequences must be strings.")

    if len(aligned_sequence_a) != len(aligned_sequence_b):
        raise ValueError("Aligned sequences must have equal lengths.")

    if not aligned_sequence_a:
        raise ValueError("Aligned sequences cannot be empty.")

    matrix = []

    for base_a, base_b in zip(aligned_sequence_a.upper(), aligned_sequence_b.upper()):
        if base_a == "-" or base_b == "-":
            value = -1
        elif base_a == base_b:
            value = 1
        else:
            value = 0

        matrix.append(value)

    return matrix


def get_alignment_summary(aligned_sequence_a: str, aligned_sequence_b: str) -> dict:
    """Return alignment match, mismatch and gap statistics."""

    matrix = create_alignment_matrix(aligned_sequence_a, aligned_sequence_b)

    matches = matrix.count(1)
    mismatches = matrix.count(0)
    gaps = matrix.count(-1)
    total = len(matrix)

    return {
        "alignment_length": total,
        "matches": matches,
        "mismatches": mismatches,
        "gaps": gaps,
        "identity_percentage": round((matches / total) * 100, 2),
        "matrix": matrix,
    }


def generate_alignment_heatmap(
    aligned_sequence_a: str,
    aligned_sequence_b: str,
    output_path: str | Path | None = None,
) -> str:
    """Generate and save an alignment heatmap image."""

    matrix = create_alignment_matrix(aligned_sequence_a, aligned_sequence_b)

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.colors import ListedColormap
    except ImportError as error:
        raise RuntimeError(
            "Matplotlib is required for heatmap generation. "
            "Install it using: python -m pip install matplotlib"
        ) from error

    if output_path is None:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = OUTPUT_DIR / "alignment_heatmap.png"
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

    figure, axis = plt.subplots(figsize=(max(8, len(matrix) * 0.35), 3))

    colors = ["#f39c12", "#e74c3c", "#2ecc71"]
    colormap = ListedColormap(colors)

    axis.imshow(
        [[value + 1 for value in matrix]],
        cmap=colormap,
        vmin=0,
        vmax=2,
        aspect="auto",
    )

    axis.set_yticks([0])
    axis.set_yticklabels(["Alignment"])

    axis.set_xticks(range(len(matrix)))
    axis.set_xticklabels(
        [str(index + 1) for index in range(len(matrix))],
        rotation=90,
    )

    axis.set_xlabel("Alignment Position")
    axis.set_title("GeneWeaver DNA Alignment Heatmap")

    figure.tight_layout()
    figure.savefig(output_path, dpi=150)
    plt.close(figure)

    return str(output_path)


__all__ = [
    "create_alignment_matrix",
    "get_alignment_summary",
    "generate_alignment_heatmap",
]
