from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User
from app.models.savings_goal import SavingsGoal

from app.schemas.goal_priority import (
    GoalPriorityResponse,
)

from app.services.goal_priority_service import (
    get_goal_priority,
)

router = APIRouter(
    prefix="/goal-priority",
    tags=["Goal Priority"],
)


@router.get(
    "/",
    response_model=GoalPriorityResponse,
)
def goal_priority(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user,
    ),
):

    goals = (
        db.query(SavingsGoal)
        .filter(
            SavingsGoal.user_id == current_user.id
        )
        .all()
    )

    return get_goal_priority(
        goals
    )