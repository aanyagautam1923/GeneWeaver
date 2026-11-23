from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

def test_week2_system_endpoint():
    response = client.get("/api/week2/system")
    assert response.status_code == 200
    assert "cpu_percent" in response.json()

def test_week2_analyze_endpoint():
    response = client.post("/api/week2/analyze", json={"sequence": "ACGT"})
    assert response.status_code == 200
    assert response.json()["stats"]["gc_percent"] == 50

def test_week2_search_endpoint():
    response = client.post("/api/week2/search", json={"sequence": "ACGTACGT", "pattern": "ACG"})
    assert response.status_code == 200
    assert response.json()["positions"] == [0, 4]

def test_week2_fasta_endpoint():
    response = client.post("/api/week2/fasta", json={"fasta": ">seq1\nACGT\n>seq2\nGGCC"})
    assert response.status_code == 200
    assert len(response.json()["records"]) == 2

def test_week2_pam_endpoint():
    response = client.post("/api/week2/pam", json={"sequence": "AAGG"})
    assert response.status_code == 200

def test_week2_alignment_endpoint():
    response = client.post("/api/week2/alignment", json={"sequence1": "ACGT", "sequence2": "ACCT"})
    assert response.status_code == 200
    assert "score" in response.json()

def test_invalid_sequence():
    response = client.post("/api/week2/analyze", json={"sequence": "INVALID"})
    assert response.status_code == 400
