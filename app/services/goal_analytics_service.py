from datetime import date
from math import ceil

from sqlalchemy.orm import Session

from app.models.savings_goal import SavingsGoal


def get_goal_analytics(
    db: Session,
    user_id: int,
):
    goals = (
        db.query(SavingsGoal)
        .filter(
            SavingsGoal.user_id == user_id
        )
        .all()
    )

    total_goals = len(goals)

    completed_goals = 0

    total_target_amount = 0
    total_saved_amount = 0
    total_remaining_amount = 0

    high_priority_goals = 0
    medium_priority_goals = 0
    low_priority_goals = 0

    monthly_saving_needed_all_goals = 0

    goals_data = []

    for goal in goals:

        total_target_amount += goal.target_amount
        total_saved_amount += goal.saved_amount

        remaining_amount = max(
            goal.target_amount - goal.saved_amount,
            0,
        )

        total_remaining_amount += remaining_amount

        progress_percentage = 0

        if goal.target_amount > 0:
            progress_percentage = (
                goal.saved_amount
                / goal.target_amount
            ) * 100

        progress_percentage = min(
            progress_percentage,
            100,
        )

        days_left = (
            goal.deadline - date.today()
        ).days

        if goal.saved_amount >= goal.target_amount:
            status = "Completed"
            completed_goals += 1
        elif days_left < 0:
            status = "Overdue"
        else:
            status = "In Progress"

        months_left = max(
            ceil(days_left / 30),
            1,
        )

        monthly_required_saving = (
            remaining_amount
            / months_left
        )

        monthly_saving_needed_all_goals += (
            monthly_required_saving
        )

        if days_left <= 90:
            priority = "High"
            high_priority_goals += 1

        elif days_left <= 180:
            priority = "Medium"
            medium_priority_goals += 1

        else:
            priority = "Low"
            low_priority_goals += 1

        expected_progress = 0

        if goal.target_amount > 0:

            total_goal_days = max(
                (
                    goal.deadline
                    - goal.created_at.date()
                ).days,
                1,
            )

            elapsed_days = max(
                (
                    date.today()
                    - goal.created_at.date()
                ).days,
                0,
            )

            expected_progress = (
                elapsed_days
                / total_goal_days
            ) * 100

        is_on_track = (
            progress_percentage
            >= expected_progress
        )

        goals_data.append(
            {
                "title": goal.title,

                "target_amount": round(
                    goal.target_amount,
                    2,
                ),

                "saved_amount": round(
                    goal.saved_amount,
                    2,
                ),

                "remaining_amount": round(
                    remaining_amount,
                    2,
                ),

                "progress_percentage": round(
                    progress_percentage,
                    2,
                ),

                "days_left": days_left,

                "monthly_required_saving": round(
                    monthly_required_saving,
                    2,
                ),

                "priority": priority,

                "status": status,

                "is_on_track": is_on_track,
            }
        )

    active_goals = (
        total_goals
        - completed_goals
    )

    overall_progress_percentage = 0

    if total_target_amount > 0:
        overall_progress_percentage = (
            total_saved_amount
            / total_target_amount
        ) * 100

    goal_completion_rate = 0

    if total_goals > 0:
        goal_completion_rate = (
            completed_goals
            / total_goals
        ) * 100

    return {
        "total_goals": total_goals,

        "completed_goals": completed_goals,

        "active_goals": active_goals,

        "total_target_amount": round(
            total_target_amount,
            2,
        ),

        "total_saved_amount": round(
            total_saved_amount,
            2,
        ),

        "total_remaining_amount": round(
            total_remaining_amount,
            2,
        ),

        "overall_progress_percentage": round(
            overall_progress_percentage,
            2,
        ),

        "goal_completion_rate": round(
            goal_completion_rate,
            2,
        ),

        "high_priority_goals":
            high_priority_goals,

        "medium_priority_goals":
            medium_priority_goals,

        "low_priority_goals":
            low_priority_goals,

        "monthly_saving_needed_all_goals":
            round(
                monthly_saving_needed_all_goals,
                2,
            ),

        "goals": goals_data,
    }