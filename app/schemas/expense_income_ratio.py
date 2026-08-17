from pydantic import BaseModel


class ExpenseIncomeRatioResponse(BaseModel):
    current_month_income: float
    current_month_expense: float
    expense_income_ratio: float
    financial_status: str
    message: str
