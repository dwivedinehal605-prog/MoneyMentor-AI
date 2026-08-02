from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.savings_goal import (
    SavingsGoalCreate,
    SavingsGoalUpdate,
    SavingsGoalResponse,
)

from app.schemas.goal_progress import (
    GoalProgressResponse,
)

from app.services.savings_goal_service import (
    create_goal,
    get_all_goals,
    get_goal,
    update_goal,
    delete_goal,
    goal_progress,
)

router = APIRouter(
    prefix="/goals",
    tags=["Savings Goals"],
)


@router.post(
    "/",
    response_model=SavingsGoalResponse,
)
def add_goal(
    goal: SavingsGoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_goal(
        db=db,
        goal=goal,
        user_id=current_user.id,
    )


@router.get(
    "/",
    response_model=list[SavingsGoalResponse],
)
def read_all_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_all_goals(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/{goal_id}",
    response_model=SavingsGoalResponse,
)
def read_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_goal(
        db=db,
        goal_id=goal_id,
        user_id=current_user.id,
    )


@router.put(
    "/{goal_id}",
    response_model=SavingsGoalResponse,
)
def edit_goal(
    goal_id: int,
    goal: SavingsGoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_goal(
        db=db,
        goal_id=goal_id,
        goal=goal,
        user_id=current_user.id,
    )


@router.delete(
    "/{goal_id}",
)
def remove_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_goal(
        db=db,
        goal_id=goal_id,
        user_id=current_user.id,
    )


@router.get(
    "/progress/{goal_id}",
    response_model=GoalProgressResponse,
)
def get_goal_progress(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return goal_progress(
        db=db,
        goal_id=goal_id,
        user_id=current_user.id,
    )