from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.dependencies.auth import (
    get_current_user,
)

from app.models.user import User

from app.services.savings_goal_service import (
    get_goal,
)

from app.services.goal_recommendation_service import (
    generate_goal_recommendation,
)

from app.schemas.goal_recommendation import (
    GoalRecommendationResponse,
)

router = APIRouter(
    prefix="/goal-recommendation",
    tags=["Goal Recommendation"],
)


@router.get(
    "/{goal_id}",
    response_model=GoalRecommendationResponse,
)
def goal_recommendation(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):

    goal = get_goal(
        db=db,
        goal_id=goal_id,
        user_id=current_user.id,
    )

    return generate_goal_recommendation(
        goal
    )