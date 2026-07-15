from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Expense title"
    )

    amount: float = Field(
        ...,
        gt=0,
        description="Expense amount"
    )

    category: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Expense category"
    )


class ExpenseUpdate(BaseModel):
    title: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    amount: float = Field(
        ...,
        gt=0
    )

    category: str = Field(
        ...,
        min_length=2,
        max_length=50
    )


class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: float
    category: str

    class Config:
        from_attributes = True