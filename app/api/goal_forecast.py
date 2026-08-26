from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.dependencies.auth import (
    get_current_user,
)

from app.models.user import User

from app.models.savings_goal import (
    SavingsGoal,
)

from app.schemas.goal_forecast import (
    GoalForecastResponse,
)

from app.services.goal_forecast_service import (
    generate_goal_forecast,
)

router = APIRouter(
    prefix="/goal-forecast",
    tags=["Goal Forecast"],
)


@router.get(
    "/",
    response_model=GoalForecastResponse,
)
def goal_forecast(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):

    goals = (
        db.query(SavingsGoal)
        .filter(
            SavingsGoal.user_id
            == current_user.id
        )
        .all()
    )

    monthly_savings_capacity = 10000

    return generate_goal_forecast(
        goals,
        monthly_savings_capacity,
    )