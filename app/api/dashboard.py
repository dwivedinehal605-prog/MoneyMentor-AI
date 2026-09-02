from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User
from app.models.expense import Expense
from app.models.income import Income

from app.schemas.dashboard import DashboardSummary

from app.services.insights_service import (
    generate_financial_insights,
)

from app.services.dashboard_service import (
    generate_dashboard_summary,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/summary",
    response_model=DashboardSummary,
)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):

    incomes = (
        db.query(Income)
        .filter(
            Income.user_id
            == current_user.id
        )
        .all()
    )

    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id
            == current_user.id
        )
        .all()
    )

    insights = (
        generate_financial_insights(
            incomes=incomes,
            expenses=expenses,
        )
    )

    dashboard_data = (
        generate_dashboard_summary(
            incomes=incomes,
            expenses=expenses,
            insights=insights,
        )
    )

    return DashboardSummary(
        **dashboard_data
    )