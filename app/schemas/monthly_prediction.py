from pydantic import BaseModel, Field


class MonthlyPredictionResponse(BaseModel):
    """
    Response schema for the Monthly Financial
    Forecast endpoint.
    """

    total_income: float = Field(
        ...,
        examples=[50000.00],
        description="Total income recorded for the user."
    )

    total_expense: float = Field(
        ...,
        examples=[32000.00],
        description="Total expenses recorded for the user."
    )

    predicted_expense: float = Field(
        ...,
        examples=[34000.00],
        description="Predicted expense for the upcoming month using Machine Learning."
    )

    predicted_savings: float = Field(
        ...,
        examples=[16000.00],
        description="Estimated savings after subtracting predicted expenses from total income."
    )

    savings_status: str = Field(
        ...,
        examples=["You are projected to save approximately ₹16000.00 this month."],
        description="Summary of the user's expected savings or deficit."
    )

    budget: float = Field(
        ...,
        examples=[40000.00],
        description="User's current monthly budget."
    )

    remaining_budget: float = Field(
        ...,
        examples=[6000.00],
        description="Estimated remaining budget after predicted expenses."
    )

    financial_score: int = Field(
        ...,
        ge=0,
        le=100,
        examples=[85],
        description="Overall financial health score between 0 and 100."
    )

    health_status: str = Field(
        ...,
        examples=["Excellent"],
        description="Financial health category based on the financial score."
    )

    recommendations: list[str] = Field(
    ...,
    examples=[[
        "Keep maintaining your current spending habits.",
        "Consider investing part of your monthly savings.",
        "Review your budget monthly for continued financial stability."
    ]],
    description="Personalized financial recommendations based on the user's financial health."
)

    forecast: str = Field(
        ...,
        examples=["Excellent! You are projected to stay within your monthly budget with approximately ₹6000.00 remaining."],
        description="AI-generated monthly financial forecast."
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "total_income": 50000.00,
                "total_expense": 32000.00,
                "predicted_expense": 34000.00,
                "predicted_savings": 16000.00,
                "savings_status": "You are projected to save approximately ₹16000.00 this month.",
                "budget": 40000.00,
                "remaining_budget": 6000.00,
                "financial_score": 85,
                "health_status": "Excellent",
                "forecast": "Excellent! You are projected to stay within your monthly budget with approximately ₹6000.00 remaining."
            }
        }
    }