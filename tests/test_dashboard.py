# tests/test_dashboard.py

from uuid import uuid4

from app.models.income import Income
from app.models.expense import Expense


def register_and_login(client):
    email = f"dashboard_{uuid4().hex}@example.com"

    response = client.post(
        "/users/register",
        json={
            "full_name": "Dashboard User",
            "email": email,
            "password": "password123",
        },
    )

    assert response.status_code in [200, 201]

    response = client.post(
        "/users/login",
        data={
            "username": email,
            "password": "password123",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.get(
        "/users/me",
        headers=headers,
    )

    assert response.status_code == 200

    user_id = response.json()["id"]

    return headers, user_id


def add_financial_data(
    db_session,
    user_id,
):
    income = Income(
        user_id=user_id,
        amount=50000,
        source="Salary",
    )

    expenses = [
        Expense(
            user_id=user_id,
            title="Rent",
            category="Housing",
            amount=10000,
        ),
        Expense(
            user_id=user_id,
            title="Groceries",
            category="Food",
            amount=5000,
        ),
        Expense(
            user_id=user_id,
            title="Transport",
            category="Transport",
            amount=3000,
        ),
    ]

    db_session.add(income)
    db_session.add_all(expenses)
    db_session.commit()


def test_dashboard_summary(
    client,
    db_session,
):
    headers, user_id = register_and_login(
        client
    )

    add_financial_data(
        db_session,
        user_id,
    )

    response = client.get(
        "/dashboard/summary",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_income"] == 50000
    assert data["total_expense"] == 18000
    assert data["balance"] == 32000


def test_dashboard_requires_authentication(
    client,
):
    response = client.get(
        "/dashboard/summary"
    )

    assert response.status_code == 401


def test_dashboard_with_no_data(
    client,
):
    headers, _ = register_and_login(
        client
    )

    response = client.get(
        "/dashboard/summary",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_income"] == 0
    assert data["total_expense"] == 0
    assert data["balance"] == 0


def test_dashboard_user_isolation(
    client,
    db_session,
):
    user_a_headers, user_a_id = (
        register_and_login(client)
    )

    user_b_headers, user_b_id = (
        register_and_login(client)
    )

    add_financial_data(
        db_session,
        user_a_id,
    )

    income = Income(
        user_id=user_b_id,
        amount=100000,
        source="Business",
    )

    expense = Expense(
        user_id=user_b_id,
        title="Shopping",
        category="Shopping",
        amount=40000,
    )

    db_session.add(income)
    db_session.add(expense)
    db_session.commit()

    response_a = client.get(
        "/dashboard/summary",
        headers=user_a_headers,
    )

    assert response_a.status_code == 200

    data_a = response_a.json()

    assert data_a["total_income"] == 50000
    assert data_a["total_expense"] == 18000
    assert data_a["balance"] == 32000

    response_b = client.get(
        "/dashboard/summary",
        headers=user_b_headers,
    )

    assert response_b.status_code == 200

    data_b = response_b.json()

    assert data_b["total_income"] == 100000
    assert data_b["total_expense"] == 40000
    assert data_b["balance"] == 60000