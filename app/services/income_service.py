from sqlalchemy.orm import Session

from app.models.income import Income
from app.schemas.income import IncomeCreate, IncomeUpdate


def create_income(db: Session, income: IncomeCreate, user_id: int):
    db_income = Income(
        source=income.source,
        amount=income.amount,
        user_id=user_id
    )

    db.add(db_income)
    db.commit()
    db.refresh(db_income)

    return db_income


def get_incomes(db: Session, user_id: int):
    return db.query(Income).filter(
        Income.user_id == user_id
    ).all()


def get_income(db: Session, income_id: int, user_id: int):
    return db.query(Income).filter(
        Income.id == income_id,
        Income.user_id == user_id
    ).first()


def update_income(
    db: Session,
    income_id: int,
    income: IncomeUpdate,
    user_id: int
):
    db_income = get_income(db, income_id, user_id)

    if not db_income:
        return None

    db_income.source = income.source
    db_income.amount = income.amount

    db.commit()
    db.refresh(db_income)

    return db_income


def delete_income(db: Session, income_id: int, user_id: int):
    db_income = get_income(db, income_id, user_id)

    if not db_income:
        return None

    db.delete(db_income)
    db.commit()

    return db_income