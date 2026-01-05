from fastapi.testclient import TestClient
from gateway.app import app
import pytest

client = TestClient(app)

# ---- MOCK DEL CLIENTE DE SERVICIOS ----

class FakeServiceClient:
    async def get(self, path):
        return {"mocked": True, "path": path}


@pytest.fixture(autouse=True)
def mock_get_client(monkeypatch):
    async def fake_get_client(service_name: str):
        return FakeServiceClient()

    monkeypatch.setattr("gateway.app.get_client", fake_get_client)


# ---- TESTS ----

def test_gateway_traffic_route():
    response = client.get("/traffic/status")
    assert response.status_code == 200
    assert response.json()["mocked"] is True


def test_gateway_energy_route():
    response = client.get("/energy/grid")
    assert response.status_code == 200
    assert response.json()["mocked"] is True


def test_gateway_water_route():
    response = client.get("/water/pressure")
    assert response.status_code == 200
    assert response.json()["mocked"] is True
