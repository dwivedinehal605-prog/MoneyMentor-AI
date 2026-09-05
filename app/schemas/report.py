from pydantic import BaseModel


class ReportSummaryResponse(BaseModel):
    month: int
    year: int

    total_income: float
    total_expense: float

    savings: float
    savings_rate: float

    top_expense_category: str
    financial_health: str

    total_transactions: int


class MonthlyReportResponse(
    ReportSummaryResponse
):
    pass