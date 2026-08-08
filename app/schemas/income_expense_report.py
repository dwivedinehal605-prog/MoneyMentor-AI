from pydantic import BaseModel, Field


class IncomeExpenseReportResponse(
    BaseModel
):
    total_income: float = Field(
        ...,
        examples=[50000.0],
    )

    total_expense: float = Field(
        ...,
        examples=[32000.0],
    )

    difference: float = Field(
        ...,
        examples=[18000.0],
    )

    status: str = Field(
        ...,
        examples=["Surplus"],
    )