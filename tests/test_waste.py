from fastapi.testclient import TestClient
from services.waste.app import app

client = TestClient(app)

def test_waste_containers():
    response = client.get("/waste/containers")
    assert response.status_code == 200
    data = response.json()
    assert "containers_total" in data

def test_waste_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
