from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.expense_anomaly import (
    ExpenseAnomalyResponse,
)

from app.services.expense_anomaly_service import (
    detect_expense_anomalies,
)


router = APIRouter(
    prefix="/anomaly",
    tags=["Expense Anomaly Detection"],
)


@router.get(
    "/expenses",
    response_model=ExpenseAnomalyResponse,
)
def expense_anomalies(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Detect unusually high expenses
    using the user's historical spending.
    """

    return detect_expense_anomalies(
        db=db,
        user_id=current_user.id,
    )