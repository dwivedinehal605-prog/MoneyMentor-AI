from collections import defaultdict
from sqlalchemy.orm import Session

from app.models.income import Income
from app.models.expense import Expense


def generate_financial_insights(db: Session, user_id: int):
    """
    Generate financial insights for the logged-in user.
    """

    incomes = db.query(Income).filter(Income.user_id == user_id).all()
    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()

    # Calculate totals
    total_income = sum(income.amount for income in incomes)
    total_expense = sum(expense.amount for expense in expenses)

    balance = total_income - total_expense

    # Savings Rate
    savings_rate = 0
    if total_income > 0:
        savings_rate = (balance / total_income) * 100

    # Highest Spending Category
    category_totals = defaultdict(float)

    for expense in expenses:
        category_totals[expense.category] += expense.amount

    highest_category = None
    highest_amount = 0

    if category_totals:
        highest_category = max(category_totals, key=category_totals.get)
        highest_amount = category_totals[highest_category]

    # Generate Insights
    insights = []

    if total_income == 0:
        insights.append("No income records found. Add your income to receive personalized insights.")

    if total_expense == 0:
        insights.append("No expenses recorded yet.")

    if savings_rate >= 30:
        insights.append("Excellent! Your savings rate is very healthy.")

    elif savings_rate >= 20:
        insights.append("Good job! You are saving more than the recommended minimum.")

    elif savings_rate > 0:
        insights.append("Your savings rate is low. Try reducing unnecessary expenses.")

    else:
        insights.append("Warning: Your expenses are equal to or greater than your income.")

    if total_expense > total_income:
        insights.append("You are spending more than you earn. Review your monthly budget.")

    if highest_category:
        insights.append(
            f"Your highest spending category is '{highest_category}' (₹{highest_amount:.2f})."
        )

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "savings_rate": round(savings_rate, 2),
        "highest_spending_category": highest_category,
        "highest_category_amount": highest_amount,
        "insights": insights
    }
