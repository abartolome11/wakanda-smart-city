from fastapi.testclient import TestClient
from services.security.app import app

client = TestClient(app)

def test_security_events():
    response = client.get("/security/events")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_security_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
