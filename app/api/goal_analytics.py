from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.dependencies.auth import (
    get_current_user,
)

from app.models.user import User

from app.schemas.goal_analytics import (
    GoalAnalyticsResponse,
)

from app.services.goal_analytics_service import (
    get_goal_analytics,
)

router = APIRouter(
    prefix="/goal-analytics",
    tags=["Goal Analytics"],
)


@router.get(
    "/",
    response_model=GoalAnalyticsResponse,
)
def goal_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return get_goal_analytics(
        db=db,
        user_id=current_user.id,
    )