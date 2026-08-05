from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user

from app.models.expense import Expense
from app.models.user import User

from app.schemas.prediction import (
    PredictionResponse,
)

from app.schemas.monthly_prediction import (
    MonthlyPredictionResponse,
)

from app.services.prediction_service import (
    predict_monthly_expense,
    monthly_financial_forecast,
)

router = APIRouter(
    prefix="/prediction",
    tags=["Prediction"],
)


# ==========================================
# Predict Next Month Expense
# ==========================================

@router.get(
    "/next-expense",
    response_model=PredictionResponse,
)
def predict_next_month_expense(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == current_user.id
        )
        .order_by(
            Expense.created_at
        )
        .all()
    )

    predicted_amount = predict_monthly_expense(expenses)

    if predicted_amount is None:

        predicted_amount = sum(
            expense.amount
            for expense in expenses
        )

        message = (
            "Not enough historical monthly data. "
            "Using current total expenses as an estimated prediction."
        )

    else:

       message = (
          "Monthly prediction generated successfully."
        )

    return PredictionResponse(
    predicted_amount=round(
        predicted_amount,
        2,
    ),
    message=message,
)

# ==========================================
# Monthly Financial Forecast
# ==========================================

@router.get(
    "/monthly",
    response_model=MonthlyPredictionResponse,
)
def monthly_prediction(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate a monthly financial
    forecast using income,
    expenses, and budget data.
    """

    return monthly_financial_forecast(
        db=db,
        user_id=current_user.id,
    )