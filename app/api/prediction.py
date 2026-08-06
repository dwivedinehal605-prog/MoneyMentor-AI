from fastapi import APIRouter, Depends, HTTPException
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

from app.schemas.spending_trend import (
    SpendingTrendResponse,
)

from app.services.prediction_service import (
    predict_monthly_expense,
    monthly_financial_forecast,
)

from app.services.trend_service import (
    get_spending_trend,
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
    """
    Predict the user's next month's
    expenses using historical data.
    """

    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == current_user.id
        )
        .order_by(
            Expense.created_at.asc()
        )
        .all()
    )

    if not expenses:
        raise HTTPException(
            status_code=404,
            detail=(
                "No expense records found. "
                "Please add expenses before requesting a prediction."
            ),
        )

    predicted_amount = predict_monthly_expense(
        expenses
    )

    if predicted_amount is None:

        predicted_amount = sum(
            expense.amount
            for expense in expenses
        )

        message = (
            "Insufficient historical monthly data. "
            "Using current total expenses as an estimated prediction."
        )

    else:

        message = (
            "Next month's expense prediction generated successfully."
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
    Generate a complete monthly
    financial forecast.
    """

    return monthly_financial_forecast(
        db=db,
        user_id=current_user.id,
    )


# ==========================================
# Spending Trend Analysis
# ==========================================

@router.get(
    "/spending-trend",
    response_model=SpendingTrendResponse,
)
def spending_trend(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Compare the current month's
    expenses with the previous month.
    """

    return get_spending_trend(
        db=db,
        user_id=current_user.id,
    )