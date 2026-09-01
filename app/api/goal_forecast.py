from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.dependencies.auth import (
    get_current_user,
)

from app.models.user import User

from app.services.goal_forecast_service import (
    get_goal_forecast,
)

router = APIRouter(
    prefix="/goal-forecast",
    tags=["Goal Forecast"],
)


@router.get("/")
def goal_forecast(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return get_goal_forecast(
        db=db,
        user_id=current_user.id,
    )