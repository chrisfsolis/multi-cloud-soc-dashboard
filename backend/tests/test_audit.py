def test_list_audit_entries(client):
    client.post("/api/alerts/ingest", json={
        "source": "aws",
        "raw": {"detail": {"type": "test", "severity": 5}}
    })
    resp = client.get("/api/audit")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert "total" in data
    assert data["total"] >= 1


def test_filter_by_entity_type(client):
    client.post("/api/alerts/ingest", json={
        "source": "aws",
        "raw": {"detail": {"type": "test", "severity": 5}}
    })
    client.post("/api/incidents", json={
        "title": "Audit Test Incident",
        "severity": "high",
        "status": "new",
    })

    resp = client.get("/api/audit", params={"entity_type": "alert"})
    assert resp.status_code == 200
    data = resp.json()
    for item in data["items"]:
        assert item["entity_type"] == "alert"

    resp2 = client.get("/api/audit", params={"entity_type": "incident"})
    assert resp2.status_code == 200
    data2 = resp2.json()
    for item in data2["items"]:
        assert item["entity_type"] == "incident"


def test_entity_audit(client):
    ingest_resp = client.post("/api/alerts/ingest", json={
        "source": "aws",
        "raw": {"detail": {"type": "test", "severity": 5}}
    })
    alert_id = ingest_resp.json()["id"]

    client.patch(f"/api/alerts/{alert_id}/status", json={"status": "investigating"})

    resp = client.get(f"/api/audit/alert/{alert_id}")
    assert resp.status_code == 200
    entries = resp.json()
    assert len(entries) >= 2
    actions = [e["action"] for e in entries]
    assert "created" in actions
    assert "status_change" in actions
