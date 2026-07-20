from pydantic import BaseModel
from datetime import datetime


class IncomeCreate(BaseModel):
    source: str
    amount: float


class IncomeUpdate(BaseModel):
    source: str
    amount: float


class IncomeResponse(BaseModel):
    id: int
    source: str
    amount: float
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True