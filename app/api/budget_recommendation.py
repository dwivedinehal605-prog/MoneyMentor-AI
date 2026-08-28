from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.dependencies.auth import (
    get_current_user,
)

from app.models.user import User
from app.models.expense import Expense

from app.schemas.budget_recommendation import (
    BudgetRecommendationResponse,
)

from app.services.budget_recommendation_service import (
    generate_budget_recommendation,
)

router = APIRouter(
    prefix="/budget-recommendation",
    tags=["Budget Recommendation"],
)


@router.get(
    "/",
    response_model=BudgetRecommendationResponse,
)
def budget_recommendation(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user,
    ),
):

    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id
            == current_user.id
        )
        .all()
    )

    return generate_budget_recommendation(
        expenses,
    )