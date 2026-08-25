from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.dependencies.auth import (
    get_current_user,
)

from app.models.user import User
from app.models.expense import Expense
from app.models.income import Income

from app.schemas.spending_coach import (
    SpendingCoachResponse,
)

from app.services.insights_service import (
    generate_financial_insights,
)

from app.services.spending_coach_service import (
    generate_spending_coach,
)

router = APIRouter(
    prefix="/spending-coach",
    tags=["AI Spending Coach"],
)


@router.get(
    "/",
    response_model=SpendingCoachResponse,
)
def spending_coach(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):

    incomes = (
        db.query(Income)
        .filter(
            Income.user_id == current_user.id
        )
        .all()
    )

    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == current_user.id
        )
        .all()
    )

    insights = generate_financial_insights(
        incomes,
        expenses,
    )

    return generate_spending_coach(
        insights
    )