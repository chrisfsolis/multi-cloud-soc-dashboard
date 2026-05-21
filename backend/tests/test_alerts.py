import pytest


def _ingest_aws_alert(client):
    return client.post("/api/alerts/ingest", json={
        "source": "aws",
        "raw": {
            "detail": {
                "type": "UnauthorizedAccess:IAMUser/MaliciousIPCaller",
                "severity": 8.0
            }
        }
    })


def _ingest_azure_alert(client):
    return client.post("/api/alerts/ingest", json={
        "source": "azure",
        "raw": {
            "properties": {
                "alertDisplayName": "Brute-force attack on Azure AD",
                "severity": "High",
                "tactics": ["Credential Access"]
            }
        }
    })


def _ingest_gcp_alert(client):
    return client.post("/api/alerts/ingest", json={
        "source": "gcp",
        "raw": {
            "finding": {
                "category": "OPEN_FIREWALL",
                "severity": "HIGH"
            }
        }
    })


def test_list_alerts_empty(client):
    resp = client.get("/api/alerts")
    assert resp.status_code == 200
    data = resp.json()
    assert data["items"] == []
    assert data["total"] == 0


def test_ingest_alert_aws(client):
    resp = _ingest_aws_alert(client)
    assert resp.status_code == 201
    data = resp.json()
    assert data["source"] == "aws"
    assert data["severity"] == "high"
    assert data["status"] == "new"
    assert "id" in data


def test_ingest_alert_azure(client):
    resp = _ingest_azure_alert(client)
    assert resp.status_code == 201
    data = resp.json()
    assert data["source"] == "azure"
    assert data["severity"] == "high"
    assert data["title"] == "Brute-force attack on Azure AD"


def test_ingest_alert_gcp(client):
    resp = _ingest_gcp_alert(client)
    assert resp.status_code == 201
    data = resp.json()
    assert data["source"] == "gcp"
    assert data["severity"] == "high"
    assert data["title"] == "OPEN_FIREWALL"


def test_list_alerts_with_data(client):
    _ingest_aws_alert(client)
    _ingest_azure_alert(client)
    resp = client.get("/api/alerts")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_get_alert(client):
    ingest_resp = _ingest_aws_alert(client)
    alert_id = ingest_resp.json()["id"]
    resp = client.get(f"/api/alerts/{alert_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == alert_id


def test_get_alert_not_found(client):
    resp = client.get("/api/alerts/nonexistent-id")
    assert resp.status_code == 404


def test_search_alerts(client):
    _ingest_aws_alert(client)
    resp = client.get("/api/alerts/search", params={"q": "Unauthorized"})
    assert resp.status_code == 200
    results = resp.json()
    assert len(results) >= 1
    assert "Unauthorized" in results[0]["title"]


def test_search_alerts_empty_query(client):
    resp = client.get("/api/alerts/search", params={"q": ""})
    assert resp.status_code == 200
    assert resp.json() == []


def test_update_alert_status(client):
    ingest_resp = _ingest_aws_alert(client)
    alert_id = ingest_resp.json()["id"]
    resp = client.patch(f"/api/alerts/{alert_id}/status", json={
        "status": "investigating"
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "investigating"


def test_assign_alert(client):
    ingest_resp = _ingest_aws_alert(client)
    alert_id = ingest_resp.json()["id"]
    resp = client.patch(f"/api/alerts/{alert_id}/assign", json={
        "assigned_to": "analyst@soc.internal"
    })
    assert resp.status_code == 200
    assert resp.json()["assigned_to"] == "analyst@soc.internal"


def test_filter_alerts_by_severity(client):
    _ingest_aws_alert(client)
    _ingest_gcp_alert(client)
    resp = client.get("/api/alerts", params={"severity": "high"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 1
    for item in data["items"]:
        assert item["severity"] == "high"


def test_filter_alerts_by_source(client):
    _ingest_aws_alert(client)
    _ingest_azure_alert(client)
    resp = client.get("/api/alerts", params={"source": "aws"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 1
    for item in data["items"]:
        assert item["source"] == "aws"
