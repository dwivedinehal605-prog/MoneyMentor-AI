def test_user_registration(client):
    response = client.post(
        "/users/register",
        json={
            "full_name": "Test User",
            "email": "test@example.com",
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["full_name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert "password" not in data


def test_user_login(client):
    client.post(
        "/users/register",
        json={
            "full_name": "Test User",
            "email": "test@example.com",
            "password": "TestPassword123",
        },
    )

    response = client.post(
        "/users/login",
        data={
            "username": "test@example.com",
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
def test_user_profile_requires_authentication(client):
    response = client.get("/users/me")

    assert response.status_code in [401, 403]


def test_user_profile_with_valid_token(client):
    client.post(
        "/users/register",
        json={
            "full_name": "Profile Test User",
            "email": "profile@example.com",
            "password": "TestPassword123",
        },
    )

    login_response = client.post(
        "/users/login",
        data={
            "username": "profile@example.com",
            "password": "TestPassword123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "profile@example.com"
    assert data["full_name"] == "Profile Test User"
    assert "password" not in data
