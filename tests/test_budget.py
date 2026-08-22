from datetime import datetime

from app.main import app


def create_test_user(client, email):
    response = client.post(
        "/users/register",
        json={
            "full_name": "Budget Test User",
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


def create_budget(client, token, month=None, year=None, amount=10000):
    now = datetime.now()

    if month is None:
        month = now.month

    if year is None:
        year = now.year

    response = client.post(
        "/budgets/",
        json={
            "month": month,
            "year": year,
            "budget_amount": amount,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    return response.json()


def test_create_budget(client):
    token = create_test_user(
        client,
        "budget_create@example.com",
    )

    budget = create_budget(
        client,
        token,
        amount=10000,
    )

    assert budget["budget_amount"] == 10000
    assert budget["user_id"] is not None
    assert budget["month"] == datetime.now().month
    assert budget["year"] == datetime.now().year


def test_create_budget_requires_authentication(client):
    response = client.post(
        "/budgets/",
        json={
            "month": datetime.now().month,
            "year": datetime.now().year,
            "budget_amount": 10000,
        },
    )

    assert response.status_code in [401, 403]


def test_create_duplicate_budget(client):
    token = create_test_user(
        client,
        "budget_duplicate@example.com",
    )

    create_budget(
        client,
        token,
        amount=10000,
    )

    response = client.post(
        "/budgets/",
        json={
            "month": datetime.now().month,
            "year": datetime.now().year,
            "budget_amount": 15000,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Budget already exists for this month."
    )


def test_create_budget_rejects_invalid_amount(client):
    token = create_test_user(
        client,
        "budget_invalid_amount@example.com",
    )

    response = client.post(
        "/budgets/",
        json={
            "month": datetime.now().month,
            "year": datetime.now().year,
            "budget_amount": 0,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 422


def test_create_budget_rejects_invalid_month(client):
    token = create_test_user(
        client,
        "budget_invalid_month@example.com",
    )

    response = client.post(
        "/budgets/",
        json={
            "month": 13,
            "year": datetime.now().year,
            "budget_amount": 10000,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 422


def test_get_current_budget(client):
    token = create_test_user(
        client,
        "budget_current@example.com",
    )

    budget = create_budget(
        client,
        token,
        amount=12000,
    )

    response = client.get(
        "/budgets/current",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == budget["id"]
    assert data["budget_amount"] == 12000


def test_get_current_budget_requires_authentication(client):
    response = client.get(
        "/budgets/current"
    )

    assert response.status_code in [401, 403]


def test_get_current_budget_not_found(client):
    token = create_test_user(
        client,
        "budget_current_missing@example.com",
    )

    response = client.get(
        "/budgets/current",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 404


def test_get_all_budgets(client):
    token = create_test_user(
        client,
        "budget_all@example.com",
    )

    now = datetime.now()

    create_budget(
        client,
        token,
        month=now.month,
        year=now.year,
        amount=10000,
    )

    response = client.get(
        "/budgets/",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["budget_amount"] == 10000


def test_update_budget(client):
    token = create_test_user(
        client,
        "budget_update@example.com",
    )

    budget = create_budget(
        client,
        token,
        amount=10000,
    )

    response = client.put(
        f"/budgets/{budget['id']}",
        json={
            "budget_amount": 15000,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == budget["id"]
    assert data["budget_amount"] == 15000


def test_update_nonexistent_budget(client):
    token = create_test_user(
        client,
        "budget_update_missing@example.com",
    )

    response = client.put(
        "/budgets/999999",
        json={
            "budget_amount": 15000,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 404


def test_delete_budget(client):
    token = create_test_user(
        client,
        "budget_delete@example.com",
    )

    budget = create_budget(
        client,
        token,
        amount=10000,
    )

    response = client.delete(
        f"/budgets/{budget['id']}",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    assert response.json()["message"] == (
        "Budget deleted successfully."
    )

    get_response = client.get(
        "/budgets/",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert get_response.status_code == 200
    assert get_response.json() == []


def test_delete_nonexistent_budget(client):
    token = create_test_user(
        client,
        "budget_delete_missing@example.com",
    )

    response = client.delete(
        "/budgets/999999",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 404


def test_budget_analysis(client):
    token = create_test_user(
        client,
        "budget_analysis@example.com",
    )

    create_budget(
        client,
        token,
        amount=10000,
    )

    response = client.post(
        "/expenses/",
        json={
            "title": "Test Food",
            "amount": 2000,
            "category": "Food",
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    response = client.get(
        "/budgets/analysis",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["budget_amount"] == 10000
    assert data["total_spent"] == 2000
    assert data["remaining_budget"] == 8000
    assert data["utilization_percentage"] == 20
    assert data["status"] == "Healthy"
    assert data["budget_exceeded"] is False
    assert data["amount_over_budget"] == 0


def test_budget_analysis_over_budget(client):
    token = create_test_user(
        client,
        "budget_over@example.com",
    )

    create_budget(
        client,
        token,
        amount=5000,
    )

    response = client.post(
        "/expenses/",
        json={
            "title": "Test Shopping",
            "amount": 7000,
            "category": "Shopping",
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    response = client.get(
        "/budgets/analysis",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["budget_amount"] == 5000
    assert data["total_spent"] == 7000
    assert data["remaining_budget"] == -2000
    assert data["budget_exceeded"] is True
    assert data["amount_over_budget"] == 2000
    assert data["status"] == "Over Budget"


def test_budget_analysis_requires_authentication(client):
    response = client.get(
        "/budgets/analysis"
    )

    assert response.status_code in [401, 403]


def test_budget_dashboard(client):
    token = create_test_user(
        client,
        "budget_dashboard@example.com",
    )

    create_budget(
        client,
        token,
        amount=10000,
    )

    response = client.post(
        "/expenses/",
        json={
            "title": "Dashboard Expense",
            "amount": 2000,
            "category": "Food",
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    response = client.get(
        "/budgets/dashboard",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["budget_amount"] == 10000
    assert data["total_spent"] == 2000
    assert data["remaining_budget"] == 8000
    assert data["utilization_percentage"] == 20
    assert data["budget_exceeded"] is False
    assert data["amount_over_budget"] == 0

    assert data["days_remaining"] >= 1
    assert data["daily_safe_spending"] >= 0


def test_budget_dashboard_requires_authentication(client):
    response = client.get(
        "/budgets/dashboard"
    )

    assert response.status_code in [401, 403]