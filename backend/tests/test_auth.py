def test_register_and_login(client):
    register_payload = {
        "email": "test@example.com",
        "password": "SecurePass123",
        "age": 28,
        "sex": "male",
    }
    reg = client.post("/api/v1/auth/register", json=register_payload)
    assert reg.status_code == 200
    assert reg.json()["success"] is True

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "SecurePass123"},
    )
    assert login.status_code == 200
    data = login.json()["data"]
    assert "access_token" in data
    assert "refresh_token" in data
