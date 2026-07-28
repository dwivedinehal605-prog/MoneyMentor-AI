from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.expense import Expense
from app.models.user import User
from app.schemas.prediction import PredictionResponse
from app.services.prediction_service import predict_monthly_expense

router = APIRouter(
    prefix="/prediction",
    tags=["Prediction"],
)


@router.get(
    "/next-expense",
    response_model=PredictionResponse,
)
def predict_expense(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    expenses = (
        db.query(Expense)
        .filter(Expense.user_id == current_user.id)
        .order_by(Expense.created_at)
        .all()
    )

    predicted_amount = predict_monthly_expense(expenses)

    if predicted_amount is None:
        raise HTTPException(
            status_code=400,
            detail="At least two months of expense data are required.",
        )

    return PredictionResponse(
        predicted_amount=predicted_amount,
        message="Monthly prediction generated successfully",
    )