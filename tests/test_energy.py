from fastapi.testclient import TestClient
from services.energy.app import app

client = TestClient(app)

def test_energy_grid():
    response = client.get("/energy/grid")
    assert response.status_code == 200
    data = response.json()
    assert "grid_load_mw" in data
    assert "renewable_percentage" in data

def test_energy_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "energy_requests_total" in response.text
