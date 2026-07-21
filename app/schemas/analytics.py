from pydantic import BaseModel
from typing import List


class DashboardSummary(BaseModel):
    total_income: float
    total_expense: float
    total_savings: float


class CategorySummary(BaseModel):
    category: str
    total: float


class MonthlySummary(BaseModel):
    month: str
    income: float
    expense: float
    savings: float