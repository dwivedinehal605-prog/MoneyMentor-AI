from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User
from app.models.expense import Expense
from app.models.income import Income
from app.models.savings_goal import SavingsGoal

from app.schemas.financial_action_plan import (
    FinancialActionPlanResponse,
)

from app.services.insights_service import (
    generate_financial_insights,
)

from app.services.financial_action_plan_service import (
    generate_action_plan,
)

router = APIRouter(
    prefix="/financial-action-plan",
    tags=["Financial Action Plan"],
)


@router.get(
    "/",
    response_model=FinancialActionPlanResponse,
)
def financial_action_plan(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user,
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

    goals = (
        db.query(SavingsGoal)
        .filter(
            SavingsGoal.user_id == current_user.id
        )
        .all()
    )

    insights = generate_financial_insights(
        incomes,
        expenses,
    )

    return generate_action_plan(
        insights,
        goals,
    )