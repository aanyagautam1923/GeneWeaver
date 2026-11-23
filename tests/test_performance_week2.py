from app.core.performance_engine import fast_search, batch_analyze, system_metrics

def test_fast_search():
    assert fast_search("ACGTACGT", "ACG") == [0, 4]
    assert fast_search("AAAAAA", "AAA") == [0, 1, 2, 3]
    assert fast_search("ACGT", "TT") == []

def test_batch():
    result = batch_analyze(["ACGT", "GGCC"])
    assert len(result) == 2
    assert result[0]["gc_percent"] == 50

def test_metrics():
    result = system_metrics()
    assert 0 <= result["ram_percent"] <= 100
    assert result["cpu_percent"] >= 0
