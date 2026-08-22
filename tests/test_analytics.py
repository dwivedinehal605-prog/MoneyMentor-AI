from uuid import uuid4

from app.models.income import Income
from app.models.expense import Expense


def register_and_login(client):
    email = f"analytics_{uuid4().hex}@example.com"

    response = client.post(
        "/users/register",
        json={
            "full_name": "Analytics User",
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
    income_amount=50000,
    expense_amounts=None,
):
    if expense_amounts is None:
        expense_amounts = [
            ("Rent", "Housing", 10000),
            ("Groceries", "Food", 5000),
            ("Transport", "Transport", 3000),
        ]

    income = Income(
        user_id=user_id,
        amount=income_amount,
        source="Salary",
    )

    expenses = [
        Expense(
            user_id=user_id,
            amount=amount,
            title=title,
            category=category,
        )
        for title, category, amount in expense_amounts
    ]

    db_session.add(income)
    db_session.add_all(expenses)
    db_session.commit()


def test_category_wise_analytics(
    client,
    db_session,
):
    headers, user_id = register_and_login(client)

    add_financial_data(
        db_session,
        user_id,
    )

    response = client.get(
        "/analytics/category-wise",
        headers=headers,
    )

    assert response.status_code == 200


def test_category_insights(
    client,
    db_session,
):
    headers, user_id = register_and_login(client)

    add_financial_data(
        db_session,
        user_id,
    )

    response = client.get(
        "/analytics/category-insights",
        headers=headers,
    )

    assert response.status_code == 200


def test_monthly_trend(
    client,
    db_session,
):
    headers, user_id = register_and_login(client)

    add_financial_data(
        db_session,
        user_id,
    )

    response = client.get(
        "/analytics/monthly-trend",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "months" in data
    assert "expenses" in data


def test_top_categories(
    client,
    db_session,
):
    headers, user_id = register_and_login(client)

    add_financial_data(
        db_session,
        user_id,
    )

    response = client.get(
        "/analytics/top-categories",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "top_categories" in data


def test_monthly_report(
    client,
    db_session,
):
    headers, user_id = register_and_login(client)

    add_financial_data(
        db_session,
        user_id,
    )

    response = client.get(
        "/analytics/monthly-report",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_income"] == 50000
    assert data["total_expense"] == 18000
    assert data["total_savings"] == 32000


def test_income_expense_report(
    client,
    db_session,
):
    headers, user_id = register_and_login(client)

    add_financial_data(
        db_session,
        user_id,
    )

    response = client.get(
        "/analytics/income-expense-report",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_income"] == 50000
    assert data["total_expense"] == 18000
    assert data["difference"] == 32000
    assert data["status"] == "Surplus"


def test_savings_summary(
    client,
    db_session,
):
    headers, user_id = register_and_login(client)

    add_financial_data(
        db_session,
        user_id,
    )

    response = client.get(
        "/analytics/savings-summary",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_income"] == 50000
    assert data["total_expense"] == 18000
    assert data["total_savings"] == 32000
    assert data["savings_rate"] == 64
    assert data["savings_status"] == "Healthy Savings"


def test_financial_health_report(
    client,
    db_session,
):
    headers, user_id = register_and_login(client)

    add_financial_data(
        db_session,
        user_id,
    )

    response = client.get(
        "/analytics/financial-health-report",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["financial_score"] == 100
    assert data["health_status"] == "Excellent"
    assert data["income"] == 50000
    assert data["expense"] == 18000
    assert data["savings"] == 32000


def test_expense_category_report(
    client,
    db_session,
):
    headers, user_id = register_and_login(client)

    add_financial_data(
        db_session,
        user_id,
    )

    response = client.get(
        "/analytics/expense-category-report",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_categories"] == 3
    assert len(data["categories"]) == 3


def test_total_expense_user_isolation(
    client,
    db_session,
):
    user_a_headers, user_a_id = register_and_login(
        client
    )

    user_b_headers, user_b_id = register_and_login(
        client
    )

    add_financial_data(
        db_session,
        user_a_id,
        income_amount=50000,
        expense_amounts=[
            ("Rent", "Housing", 10000),
        ],
    )

    add_financial_data(
        db_session,
        user_b_id,
        income_amount=60000,
        expense_amounts=[
            ("Shopping", "Shopping", 25000),
        ],
    )

    response_a = client.get(
        "/analytics/total",
        headers=user_a_headers,
    )

    assert response_a.status_code == 200
    assert response_a.json()["total_expense"] == 10000

    response_b = client.get(
        "/analytics/total",
        headers=user_b_headers,
    )

    assert response_b.status_code == 200
    assert response_b.json()["total_expense"] == 25000


def test_category_summary_user_isolation(
    client,
    db_session,
):
    user_a_headers, user_a_id = register_and_login(
        client
    )

    user_b_headers, user_b_id = register_and_login(
        client
    )

    add_financial_data(
        db_session,
        user_a_id,
        income_amount=50000,
        expense_amounts=[
            ("Rent", "Housing", 10000),
            ("Food", "Food", 5000),
        ],
    )

    add_financial_data(
        db_session,
        user_b_id,
        income_amount=60000,
        expense_amounts=[
            ("Shopping", "Shopping", 25000),
            ("Travel", "Travel", 7000),
        ],
    )

    response_a = client.get(
        "/analytics/category-summary",
        headers=user_a_headers,
    )

    assert response_a.status_code == 200

    data_a = response_a.json()

    assert len(data_a) == 2

    categories_a = {
        item["category"]: item["amount"]
        for item in data_a
    }

    assert categories_a == {
        "Housing": 10000,
        "Food": 5000,
    }

    response_b = client.get(
        "/analytics/category-summary",
        headers=user_b_headers,
    )

    assert response_b.status_code == 200

    data_b = response_b.json()

    assert len(data_b) == 2

    categories_b = {
        item["category"]: item["amount"]
        for item in data_b
    }

    assert categories_b == {
        "Shopping": 25000,
        "Travel": 7000,
    }