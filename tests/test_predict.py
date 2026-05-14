from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_predict_positive():
    r = client.post("/predict", json={"text": "This is absolutely wonderful!"})
    assert r.status_code == 200
    data = r.json()
    assert data["label"] == "POSITIVE"
    assert 0 < data["score"] <= 1

def test_predict_negative():
    r = client.post("/predict", json={"text": "This is terrible and I hate it."})
    assert r.status_code == 200
    assert r.json()["label"] == "NEGATIVE"

def test_empty_text():
    r = client.post("/predict", json={"text": "   "})
    assert r.status_code == 422

def test_drift_endpoint():
    r = client.get("/drift")
    assert r.status_code == 200