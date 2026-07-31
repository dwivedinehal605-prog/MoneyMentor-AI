from typing import List
from pydantic import BaseModel


class CategorySummary(BaseModel):
    category: str
    amount: float


class CategoryDistribution(BaseModel):
    category: str
    percentage: float


class RecentExpense(BaseModel):
    title: str
    amount: float
    category: str


class RecentIncome(BaseModel):
    source: str
    amount: float


class LargestExpense(BaseModel):
    title: str
    amount: float
    category: str


class DashboardSummary(BaseModel):
    total_income: float
    total_expense: float
    savings: float
    savings_rate: float

    financial_health_score: int
    health_status: str

    monthly_trend: str

    total_transactions: int
    total_categories: int

    average_expense: float
    average_income: float

    largest_expense: LargestExpense | None

    top_categories: List[CategorySummary]
    category_distribution: List[CategoryDistribution]

    recent_expenses: List[RecentExpense]
    recent_incomes: List[RecentIncome]