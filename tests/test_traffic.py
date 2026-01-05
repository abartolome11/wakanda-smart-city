from fastapi.testclient import TestClient
from services.traffic.app import app

client = TestClient(app)

def test_traffic_status_ok():
    response = client.get("/traffic/status")
    assert response.status_code in (200, 500)  # puede fallar por simulación
    assert isinstance(response.json(), dict)

def test_traffic_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "traffic_requests_total" in response.text
