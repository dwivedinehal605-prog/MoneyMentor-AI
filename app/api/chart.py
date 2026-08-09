from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.dependencies.auth import (
    get_current_user,
)

from app.models.user import User

from app.schemas.chart import (
    ChartResponse,
)

from app.services.chart_service import (
    get_category_expense_chart,
)

from app.services.chart_service import (
    get_monthly_expense_chart,
    get_income_vs_expense_chart,
)

from app.services.chart_service import (
    get_spending_percentage_chart,
)

router = APIRouter(
    prefix="/charts",
    tags=["Charts"],
)


@router.get(
    "/category-expense",
    response_model=ChartResponse,
)
def category_expense_chart(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return get_category_expense_chart(
        db=db,
        user_id=current_user.id,
    )

@router.get(
    "/monthly-expense",
    response_model=ChartResponse,
)
def monthly_expense_chart(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return get_monthly_expense_chart(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/income-vs-expense",
    response_model=ChartResponse,
)
def income_vs_expense_chart(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return get_income_vs_expense_chart(
        db=db,
        user_id=current_user.id,
    )

@router.get(
    "/spending-percentage",
    response_model=ChartResponse,
)
def spending_percentage_chart(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return get_spending_percentage_chart(
        db=db,
        user_id=current_user.id,
    )