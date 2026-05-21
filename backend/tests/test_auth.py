def test_register_user(client):
    resp = client.post("/api/auth/register", json={
        "username": "newuser",
        "email": "new@test.com",
        "password": "secret123",
        "role": "analyst"
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == "newuser"
    assert data["email"] == "new@test.com"
    assert data["role"] == "analyst"
    assert data["is_active"] is True


def test_register_duplicate_user(client):
    payload = {
        "username": "dupuser",
        "email": "dup@test.com",
        "password": "secret123",
        "role": "analyst"
    }
    resp1 = client.post("/api/auth/register", json=payload)
    assert resp1.status_code == 201

    resp2 = client.post("/api/auth/register", json=payload)
    assert resp2.status_code == 400
    assert "already" in resp2.json()["detail"].lower()


def test_login_success(client):
    client.post("/api/auth/register", json={
        "username": "loginuser",
        "email": "login@test.com",
        "password": "secret123",
        "role": "analyst"
    })
    resp = client.post("/api/auth/login", json={
        "username": "loginuser",
        "password": "secret123"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/api/auth/register", json={
        "username": "wrongpw",
        "email": "wrong@test.com",
        "password": "secret123",
        "role": "analyst"
    })
    resp = client.post("/api/auth/login", json={
        "username": "wrongpw",
        "password": "badpassword"
    })
    assert resp.status_code == 401


def test_me_authenticated(client, auth_headers):
    resp = client.get("/api/auth/me", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == "testadmin"
    assert data["role"] == "admin"


def test_me_unauthenticated(client):
    resp = client.get("/api/auth/me")
    assert resp.status_code == 401
