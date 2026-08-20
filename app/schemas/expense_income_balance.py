from pydantic import BaseModel


class ExpenseIncomeBalanceResponse(BaseModel):
    total_income: float
    total_expense: float
    balance_amount: float
    balance_ratio: float
    balance_score: int
    balance_status: str
    message: str
