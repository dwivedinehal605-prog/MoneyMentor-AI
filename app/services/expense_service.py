from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate

def create_expense(db: Session, expense: ExpenseCreate):
    new_expense = Expense(
        title=expense.title,
        amount=expense.amount,
        category=expense.category
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


def get_expenses(db: Session):
    return db.query(Expense).all()


def delete_expense(db: Session, expense_id: int):
    expense = db.query(Expense).filter(
        Expense.id == expense_id
    ).first()

    if not expense:
        return None

    db.delete(expense)
    db.commit()

    return expense

def update_expense(db: Session, expense_id: int, expense_data: ExpenseUpdate):
    expense = db.query(Expense).filter(
        Expense.id == expense_id
    ).first()

    if not expense:
        return None

    expense.title = expense_data.title
    expense.amount = expense_data.amount
    expense.category = expense_data.category

    db.commit()
    db.refresh(expense)

    return expense