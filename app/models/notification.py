from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func

from app.database.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    title = Column(
        String,
        nullable=False,
    )

    message = Column(
        String,
        nullable=False,
    )

    is_read = Column(
        Boolean,
        default=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )