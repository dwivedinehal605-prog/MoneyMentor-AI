from pydantic import BaseModel


class ReportSummaryResponse(
    BaseModel
):
    total_income: float
    total_expense: float
    savings: float
    savings_rate: float