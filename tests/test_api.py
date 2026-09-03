from fastapi.testclient import TestClient
from api import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_devices(monkeypatch):
    def fake_ping(ip):
        return True, 10.5, "0%"
    def fake_tcp(ip, port):
        return True

    
    monkeypatch.setattr("api.check_ping", fake_ping)
    monkeypatch.setattr("api.check_tcp", fake_tcp)

    response = client.get("/devices")
    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0
    assert data[0]["ping"] == "UP"
    assert data[0]["rtt_ms"] == 10.5
    assert data[0]["packet_loss"] == "0%"
    assert data[0]["tcp_status"] == "OPEN"   