from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "multi-cloud-soc-dashboard"}


def test_alerts():
    response = client.get("/api/alerts")
    assert response.status_code == 200
    body = response.json()
    assert body["synthetic_data"] is True
    assert len(body["items"]) >= 3
    assert {alert["provider"] for alert in body["items"]} >= {"AWS", "Azure", "GCP"}
