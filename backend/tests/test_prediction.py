def _auth_headers(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "pred@example.com", "password": "SecurePass123"},
    )
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "pred@example.com", "password": "SecurePass123"},
    )
    token = login.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_prediction_and_health_entry_persist(client):
    headers = _auth_headers(client)
    payload = {
        "symptoms_text": "high fever with cough and shortness of breath",
        "heart_rate": 120,
        "systolic_bp": 140,
        "diastolic_bp": 90,
        "temperature": 39.1,
        "spo2": 91,
        "glucose": 130,
        "weight": 72,
        "save_entry": True,
    }
    resp = client.post("/api/v1/predict", json=payload, headers=headers)
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert len(data["predictions"]) == 3
    assert "risk_score" in data
    assert "top_contributing_features" in data

    history = client.get("/api/v1/health-entries", headers=headers)
    assert history.status_code == 200
    assert len(history.json()["data"]) == 1
