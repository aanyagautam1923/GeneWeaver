from app.config import (
    get_project_info,
    create_required_directories,
)


def test_get_project_info():
    result = get_project_info()
    assert isinstance(result, dict)
    assert len(result) > 0


def test_project_info_has_name():
    result = get_project_info()
    assert "name" in result or "project_name" in result


def test_create_required_directories():
    create_required_directories()
