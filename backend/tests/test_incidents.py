def _create_incident(client):
    return client.post("/api/incidents", json={
        "title": "Test Incident",
        "severity": "high",
        "status": "new",
        "source_providers": ["aws"],
        "mitre_tactics": ["Initial Access"],
    })


def test_list_incidents_empty(client):
    resp = client.get("/api/incidents")
    assert resp.status_code == 200
    data = resp.json()
    assert data["items"] == []
    assert data["total"] == 0


def test_create_incident(client):
    resp = _create_incident(client)
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Test Incident"
    assert data["severity"] == "high"
    assert data["status"] == "new"
    assert "id" in data


def test_get_incident(client):
    create_resp = _create_incident(client)
    inc_id = create_resp.json()["id"]
    resp = client.get(f"/api/incidents/{inc_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == inc_id


def test_get_incident_not_found(client):
    resp = client.get("/api/incidents/nonexistent")
    assert resp.status_code == 404


def test_update_incident_status(client):
    create_resp = _create_incident(client)
    inc_id = create_resp.json()["id"]
    resp = client.patch(f"/api/incidents/{inc_id}/status", json={
        "status": "investigating"
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "investigating"


def test_add_incident_note(client):
    create_resp = _create_incident(client)
    inc_id = create_resp.json()["id"]
    resp = client.post(f"/api/incidents/{inc_id}/notes", json={
        "content": "Investigation started",
        "author": "analyst@soc.internal"
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["content"] == "Investigation started"
    assert data["author"] == "analyst@soc.internal"
    assert data["incident_id"] == inc_id


def test_incident_timeline(client):
    create_resp = _create_incident(client)
    inc_id = create_resp.json()["id"]
    resp = client.get(f"/api/incidents/{inc_id}/timeline")
    assert resp.status_code == 200
    timeline = resp.json()
    assert isinstance(timeline, list)
    assert len(timeline) >= 1
    assert timeline[0]["type"] == "created"


def test_export_incident(client):
    create_resp = _create_incident(client)
    inc_id = create_resp.json()["id"]
    resp = client.post(f"/api/incidents/{inc_id}/export")
    assert resp.status_code == 200
    data = resp.json()
    assert data["format"] == "markdown"
    assert "markdown" in data
    assert inc_id in data["markdown"]
    assert "generated_at" in data
