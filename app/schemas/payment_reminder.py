from datetime import date

from pydantic import BaseModel


class PaymentReminderItem(BaseModel):
    title: str
    amount: float
    category: str
    due_date: date
    days_remaining: int
    status: str
    message: str


class PaymentReminderResponse(BaseModel):
    reminders: list[PaymentReminderItem]