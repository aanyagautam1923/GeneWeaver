from app.visualization.alignment_heatmap import (
    create_alignment_matrix,
    get_alignment_summary,
)


def test_alignment_matrix():
    matrix = create_alignment_matrix("ATGC", "ATCC")

    assert len(matrix) == 4
    assert matrix == [1, 1, 0, 1]


def test_alignment_summary():
    result = get_alignment_summary("ATGC", "ATCC")

    assert result["matches"] == 3
    assert result["mismatches"] == 1
    assert result["gaps"] == 0
    assert result["identity_percentage"] == 75.0
