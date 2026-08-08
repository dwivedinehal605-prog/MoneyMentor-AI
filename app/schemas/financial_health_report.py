from pydantic import BaseModel, Field


class FinancialHealthReportResponse(
    BaseModel
):
    financial_score: int = Field(
        ...,
        examples=[85],
    )

    health_status: str = Field(
        ...,
        examples=["Excellent"],
    )

    income: float = Field(
        ...,
        examples=[50000.0],
    )

    expense: float = Field(
        ...,
        examples=[32000.0],
    )

    savings: float = Field(
        ...,
        examples=[18000.0],
    )

    recommendation: str = Field(
        ...,
        examples=[
            "Maintain your current spending habits."
        ],
    )