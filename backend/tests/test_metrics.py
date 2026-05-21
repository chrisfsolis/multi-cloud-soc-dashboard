def test_metrics_overview(client):
    resp = client.get("/api/metrics/overview")
    assert resp.status_code == 200
    data = resp.json()
    assert "total_alerts" in data
    assert "total_incidents" in data
    assert "open_incidents" in data
    assert "mttd_minutes" in data
    assert "mttr_hours" in data
    assert "false_positive_rate" in data


def test_mttd(client):
    resp = client.get("/api/metrics/mttd")
    assert resp.status_code == 200
    data = resp.json()
    assert "mttd_minutes" in data
    assert "sample_size" in data


def test_mtta(client):
    resp = client.get("/api/metrics/mtta")
    assert resp.status_code == 200
    data = resp.json()
    assert "mtta_minutes" in data
    assert "sample_size" in data


def test_mttr(client):
    resp = client.get("/api/metrics/mttr")
    assert resp.status_code == 200
    data = resp.json()
    assert "mttr_hours" in data
    assert "sample_size" in data


def test_false_positive_rate(client):
    resp = client.get("/api/metrics/false-positive-rate")
    assert resp.status_code == 200
    data = resp.json()
    assert "false_positive_rate" in data
    assert "total_alerts" in data


def test_alert_volume(client):
    resp = client.get("/api/metrics/alert-volume")
    assert resp.status_code == 200
    data = resp.json()
    assert "total" in data
    assert "by_source" in data


def test_incident_volume(client):
    resp = client.get("/api/metrics/incident-volume")
    assert resp.status_code == 200
    data = resp.json()
    assert "total" in data
    assert "by_status" in data


def test_mitre_breakdown(client):
    resp = client.get("/api/metrics/mitre-breakdown")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


def test_top_risky_assets(client):
    resp = client.get("/api/metrics/top-risky-assets")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
