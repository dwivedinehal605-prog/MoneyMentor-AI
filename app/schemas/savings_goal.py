from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class SavingsGoalCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=2,
        max_length=150,
        description="Savings goal title"
    )

    target_amount: float = Field(
        ...,
        gt=0,
        description="Target amount"
    )

    deadline: date


class SavingsGoalUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    target_amount: float | None = Field(
        default=None,
        gt=0,
    )

    saved_amount: float | None = Field(
        default=None,
        ge=0,
    )

    deadline: date | None = None


class SavingsGoalResponse(BaseModel):
    id: int
    user_id: int
    title: str
    target_amount: float
    saved_amount: float
    deadline: date
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )