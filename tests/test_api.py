from app.api.main import app


def test_api_app_exists():
    assert app is not None
    assert app.title


def test_required_api_routes():
    schema = app.openapi()
    paths = set(schema["paths"].keys())

    expected_routes = {
        "/",
        "/health",
        "/sequence/analyze",
        "/alignment",
        "/pam/detect",
        "/system/status",
    }

    assert expected_routes.issubset(paths)
