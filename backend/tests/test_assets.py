def _create_asset(client, name="test-server", risk_score=50):
    return client.post("/api/assets", json={
        "name": name,
        "type": "EC2",
        "provider": "aws",
        "environment": "production",
        "owner": "team@company.com",
        "criticality": "high",
        "risk_score": risk_score
    })


def test_list_assets_empty(client):
    resp = client.get("/api/assets")
    assert resp.status_code == 200
    data = resp.json()
    assert data["items"] == []
    assert data["total"] == 0


def test_create_and_list_assets(client):
    create_resp = _create_asset(client)
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created["name"] == "test-server"
    assert created["provider"] == "aws"

    resp = client.get("/api/assets")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["id"] == created["id"]


def test_get_asset(client):
    create_resp = _create_asset(client)
    asset_id = create_resp.json()["id"]
    resp = client.get(f"/api/assets/{asset_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == asset_id
    assert resp.json()["name"] == "test-server"


def test_get_asset_not_found(client):
    resp = client.get("/api/assets/nonexistent")
    assert resp.status_code == 404


def test_high_risk_assets(client):
    _create_asset(client, name="low-risk", risk_score=30)
    _create_asset(client, name="high-risk", risk_score=90)
    resp = client.get("/api/assets/high-risk")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["name"] == "high-risk"
    assert data[0]["risk_score"] > 70


def test_update_asset(client):
    create_resp = _create_asset(client)
    asset_id = create_resp.json()["id"]
    resp = client.patch(f"/api/assets/{asset_id}", json={
        "risk_score": 95,
        "name": "updated-server"
    })
    assert resp.status_code == 200
    assert resp.json()["risk_score"] == 95
    assert resp.json()["name"] == "updated-server"


def test_asset_risk(client):
    create_resp = _create_asset(client, risk_score=60)
    asset_id = create_resp.json()["id"]
    resp = client.get(f"/api/assets/{asset_id}/risk")
    assert resp.status_code == 200
    data = resp.json()
    assert data["asset_id"] == asset_id
    assert data["risk_score"] == 60
    assert data["alert_count"] == 0
    assert data["computed_risk_score"] == 60
