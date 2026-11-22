from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


def test_search_api_exact_match():
    response = client.post(
        "/search/",
        json={
            "reference": "ACGTACGTACGT",
            "query": "ACGT",
            "max_mismatches": 0,
            "both_strands": False,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["total_matches"] >= 1


def test_search_api_no_match():
    response = client.post(
        "/search/",
        json={
            "reference": "AAAAAAAAAAAA",
            "query": "CCCC",
            "max_mismatches": 0,
            "both_strands": False,
        },
    )

    assert response.status_code == 200
    assert response.json()["data"]["total_matches"] == 0


def test_search_api_invalid_input():
    response = client.post(
        "/search/",
        json={
            "reference": "ACGTXYZ",
            "query": "ACGT",
            "max_mismatches": 0,
            "both_strands": False,
        },
    )

    assert response.status_code == 400
