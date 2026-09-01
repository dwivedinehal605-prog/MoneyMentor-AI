from sqlalchemy.orm import Session

from app.models.savings_goal import SavingsGoal


def get_savings_goal_progress(
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

    result = []

    for goal in goals:

        progress_percentage = 0

        if goal.target_amount > 0:
            progress_percentage = round(
                (goal.saved_amount / goal.target_amount)
                * 100,
                2,
            )

        remaining_amount = max(
            goal.target_amount - goal.saved_amount,
            0,
        )

        status = (
            "Completed"
            if progress_percentage >= 100
            else "In Progress"
        )

        result.append(
            {
                "title": goal.title,
                "target_amount": goal.target_amount,
                "saved_amount": goal.saved_amount,
                "remaining_amount": remaining_amount,
                "progress_percentage": progress_percentage,
                "status": status,
            }
        )

    return {
        "goals": result
    }