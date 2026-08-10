from pydantic import BaseModel


class NotificationItem(BaseModel):
    type: str
    message: str


class NotificationResponse(BaseModel):
    notifications: list[NotificationItem]