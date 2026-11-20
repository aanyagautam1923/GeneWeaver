import app.history.history_manager as history


def test_add_and_get_history(tmp_path, monkeypatch):
    monkeypatch.setattr(
        history,
        "HISTORY_FILE",
        tmp_path / "analysis_history.json"
    )

    entry = history.add_history_entry(
        operation="sequence_analysis",
        input_data={"sequence": "ATGC"},
        result={"gc_content": 50.0},
    )

    assert isinstance(entry, dict)
    assert "id" in entry

    records = history.get_history()

    assert len(records) == 1
    assert records[0]["operation"] == "sequence_analysis"


def test_get_history_entry(tmp_path, monkeypatch):
    monkeypatch.setattr(
        history,
        "HISTORY_FILE",
        tmp_path / "analysis_history.json"
    )

    entry = history.add_history_entry(
        "alignment",
        {"sequence": "ATGC"},
        {"score": 8},
    )

    result = history.get_history_entry(entry["id"])

    assert result["id"] == entry["id"]


def test_delete_history_entry(tmp_path, monkeypatch):
    monkeypatch.setattr(
        history,
        "HISTORY_FILE",
        tmp_path / "analysis_history.json"
    )

    entry = history.add_history_entry(
        "analysis",
        {"sequence": "ATGC"},
        {"success": True},
    )

    assert history.delete_history_entry(entry["id"]) is True
    assert history.get_history_count() == 0


def test_clear_history(tmp_path, monkeypatch):
    monkeypatch.setattr(
        history,
        "HISTORY_FILE",
        tmp_path / "analysis_history.json"
    )

    history.add_history_entry(
        "analysis",
        {"sequence": "ATGC"},
        {"success": True},
    )

    history.clear_history()

    assert history.get_history_count() == 0
