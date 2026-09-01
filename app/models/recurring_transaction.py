from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy import Date

from app.database.database import Base


class RecurringTransaction(Base):
    __tablename__ = "recurring_transactions"

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

    amount = Column(
        Float,
        nullable=False,
    )

    category = Column(
        String,
        nullable=False,
    )

    transaction_type = Column(
        String,
        nullable=False,
    )  # income / expense

    frequency = Column(
        String,
        nullable=False,
    )  # monthly / weekly

    is_active = Column(
        Boolean,
        default=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    next_due_date = Column(
        Date,
        nullable=False,
    )