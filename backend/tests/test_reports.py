def test_executive_summary(client):
    resp = client.get("/api/reports/executive-summary")
    assert resp.status_code == 200
    data = resp.json()
    assert data["format"] == "markdown"
    assert "markdown" in data
    assert "generated_at" in data
    assert "Executive Summary" in data["markdown"]


def test_monthly_report(client):
    resp = client.get("/api/reports/monthly-soc")
    assert resp.status_code == 200
    data = resp.json()
    assert data["format"] == "markdown"
    assert "markdown" in data
    assert "Monthly SOC Report" in data["markdown"]


def test_incident_report(client):
    create_resp = client.post("/api/incidents", json={
        "title": "Report Test Incident",
        "severity": "high",
        "status": "investigating",
    })
    inc_id = create_resp.json()["id"]

    resp = client.get(f"/api/reports/incidents/{inc_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["format"] == "markdown"
    assert inc_id in data["markdown"]


def test_incident_report_not_found(client):
    resp = client.get("/api/reports/incidents/nonexistent")
    assert resp.status_code == 404
