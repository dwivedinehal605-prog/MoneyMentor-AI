from datetime import datetime

from pydantic import BaseModel


class RecurringTransactionCreate(
    BaseModel
):
    title: str
    amount: float
    category: str
    transaction_type: str
    frequency: str


class RecurringTransactionResponse(
    BaseModel
):
    id: int
    user_id: int
    title: str
    amount: float
    category: str
    transaction_type: str
    frequency: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True