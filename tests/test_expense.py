
def create_test_user(client, email):
    response = client.post(
        "/users/register",
        json={
            "full_name": "Expense Test User",
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


def test_create_expense(client):
    token = create_test_user(
        client,
        "create_expense@example.com"
    )

    response = client.post(
        "/expenses/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Lunch",
            "amount": 250,
            "category": "Food",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Lunch"
    assert data["amount"] == 250
    assert data["category"] == "Food"


def test_create_expense_requires_authentication(client):
    response = client.post(
        "/expenses/",
        json={
            "title": "Lunch",
            "amount": 250,
            "category": "Food",
        },
    )

    assert response.status_code in [401, 403]


def test_create_expense_rejects_invalid_amount(client):
    token = create_test_user(
        client,
        "invalid_amount@example.com"
    )

    response = client.post(
        "/expenses/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Invalid Expense",
            "amount": -100,
            "category": "Food",
        },
    )

    assert response.status_code == 422


def test_get_expenses(client):
    token = create_test_user(
        client,
        "get_expenses@example.com"
    )

    client.post(
        "/expenses/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Groceries",
            "amount": 500,
            "category": "Food",
        },
    )

    response = client.get(
        "/expenses/",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1


def test_update_expense(client):
    token = create_test_user(
        client,
        "update_expense@example.com"
    )

    create_response = client.post(
        "/expenses/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Old Expense",
            "amount": 300,
            "category": "Food",
        },
    )

    assert create_response.status_code == 200

    expense_id = create_response.json()["id"]

    response = client.put(
        f"/expenses/{expense_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Updated Expense",
            "amount": 450,
            "category": "Shopping",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == expense_id
    assert data["title"] == "Updated Expense"
    assert data["amount"] == 450
    assert data["category"] == "Shopping"


def test_delete_expense(client):
    token = create_test_user(
        client,
        "delete_expense@example.com"
    )

    create_response = client.post(
        "/expenses/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Delete Me",
            "amount": 200,
            "category": "Food",
        },
    )

    assert create_response.status_code == 200

    expense_id = create_response.json()["id"]

    response = client.delete(
        f"/expenses/{expense_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    assert response.json()["message"] == "Expense deleted successfully"


def test_update_nonexistent_expense(client):
    token = create_test_user(
        client,
        "update_missing@example.com"
    )

    response = client.put(
        "/expenses/999999",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Updated Expense",
            "amount": 500,
            "category": "Food",
        },
    )

    assert response.status_code == 404


def test_delete_nonexistent_expense(client):
    token = create_test_user(
        client,
        "delete_missing@example.com"
    )

    response = client.delete(
        "/expenses/999999",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 404