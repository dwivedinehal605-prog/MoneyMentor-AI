from datetime import date, timedelta


def create_test_user(client, email):
    response = client.post(
        "/users/register",
        json={
            "full_name": "Savings Goal Test User",
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


def create_goal(client, token, title="Emergency Fund", target=50000):
    response = client.post(
        "/goals/",
        json={
            "title": title,
            "target_amount": target,
            "deadline": (
                date.today() + timedelta(days=120)
            ).isoformat(),
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    return response.json()


def test_create_savings_goal(client):
    token = create_test_user(
        client,
        "goal_create@example.com",
    )

    goal = create_goal(
        client,
        token,
    )

    assert goal["title"] == "Emergency Fund"
    assert goal["target_amount"] == 50000
    assert goal["saved_amount"] == 0
    assert goal["user_id"] is not None


def test_savings_goals_require_authentication(client):
    response = client.get("/goals/")

    assert response.status_code in [401, 403]


def test_get_all_savings_goals(client):
    token = create_test_user(
        client,
        "goal_all@example.com",
    )

    create_goal(
        client,
        token,
        title="Emergency Fund",
    )

    response = client.get(
        "/goals/",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == "Emergency Fund"


def test_get_savings_goal(client):
    token = create_test_user(
        client,
        "goal_get@example.com",
    )

    goal = create_goal(
        client,
        token,
    )

    response = client.get(
        f"/goals/{goal['id']}",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == goal["id"]
    assert data["title"] == "Emergency Fund"
    assert data["target_amount"] == 50000


def test_update_savings_goal(client):
    token = create_test_user(
        client,
        "goal_update@example.com",
    )

    goal = create_goal(
        client,
        token,
    )

    response = client.put(
        f"/goals/{goal['id']}",
        json={
            "saved_amount": 10000,
            "target_amount": 60000,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["saved_amount"] == 10000
    assert data["target_amount"] == 60000


def test_update_goal_rejects_saved_amount_over_target(client):
    token = create_test_user(
        client,
        "goal_invalid_update@example.com",
    )

    goal = create_goal(
        client,
        token,
    )

    response = client.put(
        f"/goals/{goal['id']}",
        json={
            "saved_amount": 60000,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 400


def test_get_goal_progress(client):
    token = create_test_user(
        client,
        "goal_progress@example.com",
    )

    goal = create_goal(
        client,
        token,
        target=50000,
    )

    client.put(
        f"/goals/{goal['id']}",
        json={
            "saved_amount": 10000,
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    response = client.get(
        f"/goals/progress/{goal['id']}",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Emergency Fund"
    assert data["target_amount"] == 50000
    assert data["saved_amount"] == 10000
    assert data["remaining_amount"] == 40000
    assert data["progress_percentage"] == 20
    assert data["days_remaining"] >= 1
    assert data["required_monthly_saving"] > 0
    assert data["status"] == "Needs Attention"


def test_get_goal_dashboard(client):
    token = create_test_user(
        client,
        "goal_dashboard@example.com",
    )

    goal = create_goal(
        client,
        token,
        target=50000,
    )

    response = client.get(
        f"/goals/dashboard/{goal['id']}",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Emergency Fund"
    assert data["target_amount"] == 50000
    assert data["saved_amount"] == 0
    assert data["remaining_amount"] == 50000
    assert data["progress_percentage"] == 0
    assert data["status"] == "Needs Attention"
    assert data["days_remaining"] >= 1
    assert data["recommended_daily_saving"] > 0
    assert data["recommended_monthly_saving"] > 0


def test_get_nonexistent_goal(client):
    token = create_test_user(
        client,
        "goal_missing@example.com",
    )

    response = client.get(
        "/goals/999999",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 404


def test_delete_savings_goal(client):
    token = create_test_user(
        client,
        "goal_delete@example.com",
    )

    goal = create_goal(
        client,
        token,
    )

    response = client.delete(
        f"/goals/{goal['id']}",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Savings goal deleted successfully."
    )

    get_response = client.get(
        "/goals/",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert get_response.status_code == 200
    assert get_response.json() == []