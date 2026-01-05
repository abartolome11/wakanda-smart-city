from fastapi.testclient import TestClient
from services.water.app import app

client = TestClient(app)

def test_water_pressure():
    response = client.get("/water/pressure")
    assert response.status_code == 200
    data = response.json()
    assert "pressure_bar" in data

def test_water_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
