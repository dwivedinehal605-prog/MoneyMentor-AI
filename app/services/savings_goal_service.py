from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.savings_goal import SavingsGoal

from app.schemas.savings_goal import (
    SavingsGoalCreate,
    SavingsGoalUpdate,
)


def create_goal(
    db: Session,
    goal: SavingsGoalCreate,
    user_id: int,
):
    db_goal = SavingsGoal(
        user_id=user_id,
        title=goal.title,
        target_amount=goal.target_amount,
        saved_amount=0,
        deadline=goal.deadline,
    )

    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)

    return db_goal


def get_all_goals(
    db: Session,
    user_id: int,
):
    return (
        db.query(SavingsGoal)
        .filter(
            SavingsGoal.user_id == user_id
        )
        .order_by(
            SavingsGoal.created_at.desc()
        )
        .all()
    )


def get_goal(
    db: Session,
    goal_id: int,
    user_id: int,
):
    goal = (
        db.query(SavingsGoal)
        .filter(
            SavingsGoal.id == goal_id,
            SavingsGoal.user_id == user_id,
        )
        .first()
    )

    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Savings goal not found.",
        )

    return goal


def update_goal(
    db: Session,
    goal_id: int,
    goal: SavingsGoalUpdate,
    user_id: int,
):
    db_goal = get_goal(
        db=db,
        goal_id=goal_id,
        user_id=user_id,
    )

    # Determine final values after update
    new_target = (
        goal.target_amount
        if goal.target_amount is not None
        else db_goal.target_amount
    )

    new_saved = (
        goal.saved_amount
        if goal.saved_amount is not None
        else db_goal.saved_amount
    )

    # Validation
    if new_saved > new_target:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Saved amount cannot exceed target amount.",
        )

    update_data = goal.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            db_goal,
            key,
            value,
        )

    db.commit()
    db.refresh(db_goal)

    return db_goal


def delete_goal(
    db: Session,
    goal_id: int,
    user_id: int,
):
    db_goal = get_goal(
        db=db,
        goal_id=goal_id,
        user_id=user_id,
    )

    db.delete(db_goal)
    db.commit()

    return {
        "message": "Savings goal deleted successfully."
    }


def goal_progress(
    db: Session,
    goal_id: int,
    user_id: int,
):
    goal = get_goal(
        db=db,
        goal_id=goal_id,
        user_id=user_id,
    )

    progress_percentage = (
        (goal.saved_amount / goal.target_amount) * 100
        if goal.target_amount > 0
        else 0
    )

    remaining_amount = (
        goal.target_amount - goal.saved_amount
    )

    if progress_percentage >= 100:
        status_text = "Goal Achieved"

    elif progress_percentage >= 80:
        status_text = "Almost Complete"

    elif progress_percentage >= 50:
        status_text = "On Track"

    else:
        status_text = "Started"

    return {
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
        "status": status_text,
    }
