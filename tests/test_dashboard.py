from app.dashboard import (
    get_dashboard_overview,
    analyze_dashboard_sequence,
    get_dashboard_stats,
    get_system_status,
)


def test_dashboard_overview():
    result = get_dashboard_overview()

    assert isinstance(result, dict)
    assert "project" in result
    assert "processing_mode" in result


def test_dashboard_sequence_analysis():
    result = analyze_dashboard_sequence("ATGCATGC")

    assert result["success"] is True
    assert "metrics" in result


def test_dashboard_stats():
    result = get_dashboard_stats("ATGCATGC")

    assert isinstance(result, dict)
    assert "project_name" in result
    assert "sequence_metrics" in result


def test_system_status():
    result = get_system_status()

    assert isinstance(result, dict)
    assert result["status"] == "online"
    assert "gpu_available" in result
