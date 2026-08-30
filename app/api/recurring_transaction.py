from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.recurring_transaction import (
    RecurringTransactionCreate,
    RecurringTransactionResponse,
)

from app.services.recurring_transaction_service import (
    create_recurring_transaction,
    get_recurring_transactions,
    delete_recurring_transaction,
)

router = APIRouter(
    prefix="/recurring-transactions",
    tags=["Recurring Transactions"],
)


@router.post(
    "/",
    response_model=RecurringTransactionResponse,
)
def create_transaction(
    data: RecurringTransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_recurring_transaction(
        db=db,
        user_id=current_user.id,
        data=data,
    )


@router.get(
    "/",
    response_model=List[RecurringTransactionResponse],
)
def get_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_recurring_transactions(
        db=db,
        user_id=current_user.id,
    )


@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = delete_recurring_transaction(
        db=db,
        transaction_id=transaction_id,
        user_id=current_user.id,
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Recurring transaction not found",
        )

    return result