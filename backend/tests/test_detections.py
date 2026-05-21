def _create_detection(client, rule_id="det-test-001"):
    return client.post("/api/detections", json={
        "id": rule_id,
        "name": "Test Brute Force Rule",
        "description": "Detect brute force attempts",
        "mitre_technique": "T1110",
        "mitre_tactic": "Credential Access",
        "severity": "high",
        "enabled": True,
        "conditions": {
            "alert_title_contains": ["brute-force", "failed login"],
            "source": "aws"
        },
        "actions": ["create_incident"]
    })


def test_list_detections(client):
    resp = client.get("/api/detections")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert "total" in data


def test_create_and_list_detections(client):
    create_resp = _create_detection(client)
    assert create_resp.status_code == 201

    resp = client.get("/api/detections")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 1


def test_get_detection(client):
    _create_detection(client)
    resp = client.get("/api/detections/det-test-001")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == "det-test-001"
    assert data["name"] == "Test Brute Force Rule"


def test_get_detection_not_found(client):
    resp = client.get("/api/detections/nonexistent")
    assert resp.status_code == 404


def test_test_detection_match(client):
    _create_detection(client)
    resp = client.post("/api/detections/test", json={
        "rule_id": "det-test-001",
        "event": {
            "title": "brute-force attack detected",
            "source": "aws"
        }
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["matched"] is True
    assert len(data["matched_fields"]) >= 1


def test_test_detection_no_match(client):
    _create_detection(client)
    resp = client.post("/api/detections/test", json={
        "rule_id": "det-test-001",
        "event": {
            "title": "normal login",
            "source": "gcp"
        }
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["matched"] is False


def test_reload_detections(client):
    resp = client.post("/api/detections/reload")
    if resp.status_code == 200:
        data = resp.json()
        assert "reloaded" in data
    else:
        assert resp.status_code == 404
