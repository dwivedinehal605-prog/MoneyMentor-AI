from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.database.database import (
    get_db,
)

from app.dependencies.auth import (
    get_current_user,
)

from app.models.user import User
from app.models.expense import Expense
from app.models.income import Income

from app.schemas.advisor import (
    AdvisorResponse,
)

from app.services.advisor_service import (
    generate_financial_advice,
)

router = APIRouter(
    prefix="/advisor",
    tags=["AI Advisor"],
)


@router.get(
    "",
    response_model=AdvisorResponse,
)
def get_advice(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user,
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

    return generate_financial_advice(
        incomes,
        expenses,
    )