def _create_playbook(client, approval_required=True):
    return client.post("/api/playbooks", json={
        "name": "Test Playbook",
        "description": "Automated response playbook",
        "trigger": "manual",
        "approval_required": approval_required,
        "steps": [
            {"order": 1, "action": "isolate", "description": "Isolate host"},
            {"order": 2, "action": "notify", "description": "Notify SOC team"},
        ],
        "created_by": "admin@soc.internal"
    })


def test_list_playbooks(client):
    resp = client.get("/api/playbooks")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert "total" in data


def test_create_playbook(client):
    resp = _create_playbook(client)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Test Playbook"
    assert data["approval_required"] is True


def test_get_playbook(client):
    create_resp = _create_playbook(client)
    pb_id = create_resp.json()["id"]
    resp = client.get(f"/api/playbooks/{pb_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == pb_id


def test_run_playbook(client):
    create_resp = _create_playbook(client, approval_required=True)
    pb_id = create_resp.json()["id"]
    resp = client.post(f"/api/playbooks/{pb_id}/run", json={
        "triggered_by": "manual"
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["status"] == "awaiting_approval"
    assert data["playbook_id"] == pb_id


def test_run_playbook_no_approval(client):
    create_resp = _create_playbook(client, approval_required=False)
    pb_id = create_resp.json()["id"]
    resp = client.post(f"/api/playbooks/{pb_id}/run", json={
        "triggered_by": "manual"
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["status"] == "running"


def test_approve_run(client):
    create_resp = _create_playbook(client, approval_required=True)
    pb_id = create_resp.json()["id"]
    run_resp = client.post(f"/api/playbooks/{pb_id}/run", json={
        "triggered_by": "manual"
    })
    run_id = run_resp.json()["id"]

    resp = client.post(f"/api/playbooks/runs/{run_id}/approve")
    assert resp.status_code == 200
    assert resp.json()["status"] == "running"


def test_cancel_run(client):
    create_resp = _create_playbook(client, approval_required=True)
    pb_id = create_resp.json()["id"]
    run_resp = client.post(f"/api/playbooks/{pb_id}/run", json={
        "triggered_by": "manual"
    })
    run_id = run_resp.json()["id"]

    resp = client.post(f"/api/playbooks/runs/{run_id}/cancel")
    assert resp.status_code == 200
    assert resp.json()["status"] == "cancelled"


def test_list_runs(client):
    create_resp = _create_playbook(client)
    pb_id = create_resp.json()["id"]
    client.post(f"/api/playbooks/{pb_id}/run", json={"triggered_by": "manual"})

    resp = client.get("/api/playbooks/runs")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 1
