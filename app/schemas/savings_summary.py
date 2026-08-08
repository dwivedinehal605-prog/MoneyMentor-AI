from pydantic import BaseModel, Field


class SavingsSummaryResponse(
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

    total_savings: float = Field(
        ...,
        examples=[18000.0],
    )

    savings_rate: float = Field(
        ...,
        examples=[36.0],
    )

    savings_status: str = Field(
        ...,
        examples=[
            "Healthy Savings"
        ],
    )