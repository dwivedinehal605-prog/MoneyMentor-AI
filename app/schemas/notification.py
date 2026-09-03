from pydantic import BaseModel


class Notification(BaseModel):
    type: str
    message: str

    class Config:
        from_attributes = True


class NotificationResponse(BaseModel):
    total_notifications: int
    notifications: list[Notification]

    class Config:
        from_attributes = True