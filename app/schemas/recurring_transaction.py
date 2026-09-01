from datetime import date
from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class RecurringTransactionCreate(
    BaseModel
):
    title: str
    amount: float
    category: str

    transaction_type: Literal[
        "income",
        "expense",
    ]

    frequency: Literal[
        "daily",
        "weekly",
        "monthly",
        "yearly",
    ]

    next_due_date: date


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
    next_due_date: date
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True