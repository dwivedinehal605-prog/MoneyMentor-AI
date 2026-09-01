from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.dependencies.auth import get_current_user

from app.models.user import User

from app.services.savings_goal_progress_service import (
    get_savings_goal_progress,
)

router = APIRouter(
    prefix="/savings-goals",
    tags=["Savings Goal Progress"],
)


@router.get("/progress")
def savings_goal_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return get_savings_goal_progress(
        db=db,
        user_id=current_user.id,
    )