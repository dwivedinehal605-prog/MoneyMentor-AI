from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class BudgetCreate(BaseModel):
    month: int = Field(
        ...,
        ge=1,
        le=12,
        description="Budget month (1-12)"
    )

    year: int = Field(
        ...,
        ge=2000,
        le=2100,
        description="Budget year"
    )

    budget_amount: float = Field(
        ...,
        gt=0,
        description="Monthly budget amount"
    )


class BudgetUpdate(BaseModel):
    budget_amount: float = Field(..., gt=0)


class BudgetResponse(BaseModel):
    id: int
    user_id: int
    month: int
    year: int
    budget_amount: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)