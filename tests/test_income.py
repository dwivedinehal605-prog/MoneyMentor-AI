def create_test_user(client, email="income_test@example.com"):
    response = client.post(
        "/users/register",
        json={
            "full_name": "Income Test User",
            "email": email,
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 200

    login_response = client.post(
        "/users/login",
        data={
            "username": email,
            "password": "TestPassword123",
        },
    )

    assert login_response.status_code == 200

    return login_response.json()["access_token"]


def test_create_income(client):
    token = create_test_user(client)

    response = client.post(
        "/income/",
        json={
            "source": "Salary",
            "amount": 10000,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["source"] == "Salary"
    assert data["amount"] == 10000
    assert "id" in data
    assert "created_at" in data
    assert "user_id" in data


def test_create_income_requires_authentication(client):
    response = client.post(
        "/income/",
        json={
            "source": "Salary",
            "amount": 10000,
        },
    )

    assert response.status_code in [401, 403]


def test_get_incomes(client):
    token = create_test_user(
        client,
        email="get_income@example.com"
    )

    client.post(
        "/income/",
        json={
            "source": "Salary",
            "amount": 10000,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    response = client.get(
        "/income/",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1

    assert data[0]["source"] == "Salary"
    assert data[0]["amount"] == 10000


def test_get_income_by_id(client):
    token = create_test_user(
        client,
        email="get_single_income@example.com"
    )

    create_response = client.post(
        "/income/",
        json={
            "source": "Freelancing",
            "amount": 5000,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert create_response.status_code == 200

    income_id = create_response.json()["id"]

    response = client.get(
        f"/income/{income_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == income_id
    assert data["source"] == "Freelancing"
    assert data["amount"] == 5000


def test_get_income_requires_authentication(client):
    response = client.get("/income/1")

    assert response.status_code in [401, 403]


def test_update_income(client):
    token = create_test_user(
        client,
        email="update_income@example.com"
    )

    create_response = client.post(
        "/income/",
        json={
            "source": "Freelancing",
            "amount": 5000,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert create_response.status_code == 200

    income_id = create_response.json()["id"]

    response = client.put(
        f"/income/{income_id}",
        json={
            "source": "Updated Salary",
            "amount": 15000,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == income_id
    assert data["source"] == "Updated Salary"
    assert data["amount"] == 15000


def test_delete_income(client):
    token = create_test_user(
        client,
        email="delete_income@example.com"
    )

    create_response = client.post(
        "/income/",
        json={
            "source": "Bonus",
            "amount": 3000,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert create_response.status_code == 200

    income_id = create_response.json()["id"]

    response = client.delete(
        f"/income/{income_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Income deleted successfully"


def test_get_nonexistent_income(client):
    token = create_test_user(
        client,
        email="nonexistent_income@example.com"
    )

    response = client.get(
        "/income/999999",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 404

    assert response.json()["detail"] == "Income not found"


def test_update_nonexistent_income(client):
    token = create_test_user(
        client,
        email="update_nonexistent_income@example.com"
    )

    response = client.put(
        "/income/999999",
        json={
            "source": "Salary",
            "amount": 10000,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 404

    assert response.json()["detail"] == "Income not found"


def test_delete_nonexistent_income(client):
    token = create_test_user(
        client,
        email="delete_nonexistent_income@example.com"
    )

    response = client.delete(
        "/income/999999",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 404

    assert response.json()["detail"] == "Income not found"