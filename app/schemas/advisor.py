from typing import List

from pydantic import BaseModel


class AdvisorResponse(
    BaseModel
):
    advice: List[str]