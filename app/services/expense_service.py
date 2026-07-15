from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate


def get_expense_by_id(db: Session, expense_id: int):
    return db.query(Expense).filter(Expense.id == expense_id).first()


def create_expense(db: Session, expense: ExpenseCreate):
    new_expense = Expense(
        title=expense.title,
        amount=expense.amount,
        category=expense.category
    )

    try:
        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)
        return new_expense

    except SQLAlchemyError:
        db.rollback()
        raise


def get_expenses(db: Session):
    return db.query(Expense).all()


def update_expense(db: Session, expense_id: int, expense_data: ExpenseUpdate):
    expense = get_expense_by_id(db, expense_id)

    if expense is None:
        return None

    expense.title = expense_data.title
    expense.amount = expense_data.amount
    expense.category = expense_data.category

    try:
        db.commit()
        db.refresh(expense)
        return expense

    except SQLAlchemyError:
        db.rollback()
        raise


def delete_expense(db: Session, expense_id: int):
    expense = get_expense_by_id(db, expense_id)

    if expense is None:
        return None

    try:
        db.delete(expense)
        db.commit()
        return expense

    except SQLAlchemyError:
        db.rollback()
        raise