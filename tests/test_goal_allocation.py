from datetime import date, timedelta
from types import SimpleNamespace

from app.services.goal_allocation_service import (
    generate_goal_allocation,
)


def create_goal(
    title,
    target_amount,
    saved_amount,
    days_left,
):
    return SimpleNamespace(
        title=title,
        target_amount=target_amount,
        saved_amount=saved_amount,
        deadline=date.today() + timedelta(days=days_left),
    )


def test_goal_allocation():

    goals = [
        create_goal(
            "Emergency Fund",
            100000,
            20000,
            180,
        ),
        create_goal(
            "Laptop",
            60000,
            10000,
            120,
        ),
    ]

    result = generate_goal_allocation(
        goals,
        monthly_savings_capacity=20000,
    )

    assert result["monthly_savings_capacity"] == 20000
    assert result["total_allocated"] > 0
    assert len(result["allocations"]) == 2


def test_goal_allocation_no_goals():

    result = generate_goal_allocation(
        [],
        monthly_savings_capacity=20000,
    )

    assert result["monthly_savings_capacity"] == 0
    assert result["total_allocated"] == 0
    assert result["remaining_capacity"] == 0
    assert result["allocations"] == []


def test_goal_allocation_completed_goal_ignored():

    goals = [
        create_goal(
            "Emergency Fund",
            100000,
            100000,
            180,
        ),
        create_goal(
            "Laptop",
            60000,
            10000,
            120,
        ),
    ]

    result = generate_goal_allocation(
        goals,
        monthly_savings_capacity=20000,
    )

    assert len(result["allocations"]) == 1
    assert (
        result["allocations"][0]["goal"]
        == "Laptop"
    )


def test_goal_allocation_allocation_sum():

    goals = [
        create_goal(
            "Emergency Fund",
            100000,
            10000,
            180,
        ),
        create_goal(
            "Laptop",
            50000,
            5000,
            120,
        ),
    ]

    result = generate_goal_allocation(
        goals,
        monthly_savings_capacity=15000,
    )

    assert round(
        result["total_allocated"],
        2,
    ) <= 15000