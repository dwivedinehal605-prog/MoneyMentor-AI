from pydantic import BaseModel


class PredictionResponse(BaseModel):
    predicted_amount: float
    message: str