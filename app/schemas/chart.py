from pydantic import BaseModel


class ChartItem(BaseModel):

    label: str

    value: float


class ChartResponse(BaseModel):

    data: list[ChartItem]