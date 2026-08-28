from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.dependencies.auth import (
    get_current_user,
)

from app.models.user import User
from app.models.expense import Expense
from app.models.budget import Budget

from app.schemas.budget_alert import (
    BudgetAlertResponse,
)

from app.services.budget_alert_service import (
    generate_budget_alert,
)

router = APIRouter(
    prefix="/budget-alert",
    tags=["Budget Alert"],
)


@router.get(
    "/",
    response_model=BudgetAlertResponse,
)
def budget_alert(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user,
    ),
):

    budget = (
        db.query(Budget)
        .filter(
            Budget.user_id
            == current_user.id
        )
        .order_by(
            Budget.id.desc()
        )
        .first()
    )

    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id
            == current_user.id
        )
        .all()
    )

    return generate_budget_alert(
        budget,
        expenses,
    )