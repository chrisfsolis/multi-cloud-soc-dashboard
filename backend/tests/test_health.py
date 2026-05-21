def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["version"] == "1.0.0"
    assert "checked_at" in data


def test_health_dependencies(client):
    resp = client.get("/api/health/dependencies")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] in ("healthy", "degraded")
    assert "dependencies" in data
    assert len(data["dependencies"]) >= 1
    db_dep = data["dependencies"][0]
    assert db_dep["name"] == "database"
    assert db_dep["status"] == "healthy"
    assert db_dep["latency_ms"] >= 0
