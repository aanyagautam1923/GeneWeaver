import pytest

from app.metrics import calculate_all_metrics, get_basic_metrics


def test_calculate_all_metrics():
    result = calculate_all_metrics("ATGCATGC")
    assert isinstance(result, dict)
    assert len(result) > 0


def test_metrics_sequence_length():
    result = calculate_all_metrics("ATGCATGC")
    assert result["sequence_length"] == 8


def test_metrics_gc_content():
    result = calculate_all_metrics("ATGC")
    assert result["gc_content"] == 50.0


def test_metrics_tm():
    result = calculate_all_metrics("ATGC")
    assert "melting_temperature" in result or "tm" in result


def test_get_basic_metrics():
    result = get_basic_metrics("ATGC")
    assert isinstance(result, dict)


def test_invalid_sequence():
    with pytest.raises(ValueError):
        calculate_all_metrics("ATGX")
