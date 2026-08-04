from collections import defaultdict

from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.income import Income
from app.models.budget import Budget
from app.models.savings_goal import SavingsGoal


def generate_recommendations(
    db: Session,
    user_id: int,
):
    recommendations = []

    # =====================================
    # Income Analysis
    # =====================================

    incomes = (
        db.query(Income)
        .filter(
            Income.user_id == user_id
        )
        .all()
    )

    total_income = sum(
        income.amount
        for income in incomes
    )

    # =====================================
    # Expense Analysis
    # =====================================

    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == user_id
        )
        .all()
    )

    total_expense = sum(
        expense.amount
        for expense in expenses
    )

    savings = (
        total_income -
        total_expense
    )

    savings_rate = (
        (savings / total_income) * 100
        if total_income > 0
        else 0
    )

    # =====================================
    # Financial Health
    # =====================================

    if savings_rate >= 40:

        financial_health = "Excellent"

    elif savings_rate >= 20:

        financial_health = "Good"

    elif savings_rate >= 10:

        financial_health = "Average"

    else:

        financial_health = "Needs Improvement"

    # =====================================
    # Savings Recommendation
    # =====================================

    if total_income == 0:

        recommendations.append(
            "No income has been recorded yet. Add your income to receive more accurate financial recommendations."
        )

    elif savings_rate < 20:

        recommendations.append(
            f"Your savings rate is {savings_rate:.2f}%. Try saving at least 20% of your monthly income."
        )

    else:

        recommendations.append(
            f"Great job! Your savings rate is {savings_rate:.2f}%."
        )

    # =====================================
    # Budget Analysis
    # =====================================

    latest_budget = (
        db.query(Budget)
        .filter(
            Budget.user_id == user_id
        )
        .order_by(
            Budget.created_at.desc()
        )
        .first()
    )

    if latest_budget:

        remaining_budget = (
            latest_budget.budget_amount -
            total_expense
        )

        if remaining_budget < 0:

            recommendations.append(
                f"You have exceeded your budget by ₹{abs(remaining_budget):.2f}. Reduce unnecessary expenses."
            )

        else:

            recommendations.append(
                f"You still have ₹{remaining_budget:.2f} remaining in your monthly budget."
            )

    # =====================================
    # Savings Goal Analysis
    # =====================================

    goals = (
        db.query(SavingsGoal)
        .filter(
            SavingsGoal.user_id == user_id
        )
        .all()
    )

    for goal in goals:

        progress = (
            (goal.saved_amount / goal.target_amount) * 100
            if goal.target_amount > 0
            else 0
        )

        remaining = (
            goal.target_amount -
            goal.saved_amount
        )

        if progress >= 100:

            recommendations.append(
                f"Congratulations! You have achieved your goal '{goal.title}'."
            )

        elif progress >= 80:

            recommendations.append(
                f"You're very close to achieving '{goal.title}'. Only ₹{remaining:.2f} remaining."
            )

        elif progress >= 50:

            recommendations.append(
                f"You have completed {progress:.2f}% of your '{goal.title}' goal. Keep going!"
            )

        else:

            recommendations.append(
                f"You have saved ₹{goal.saved_amount:.2f} out of ₹{goal.target_amount:.2f} for '{goal.title}'. Increase your monthly savings to reach your goal faster."
            )

    # =====================================
    # Expense Category Analysis
    # =====================================

    category_totals = defaultdict(float)

    for expense in expenses:

        category_totals[
            expense.category
        ] += expense.amount

    if category_totals:

        highest_category = max(
            category_totals,
            key=category_totals.get
        )

        highest_amount = (
            category_totals[
                highest_category
            ]
        )

        recommendations.append(
            f"{highest_category} is your highest spending category "
            f"(₹{highest_amount:.2f}). Consider reducing expenses in this category."
        )

    # =====================================
    # Expense vs Income Analysis
    # =====================================

    if total_income > 0:

        expense_ratio = (
            (total_expense / total_income) * 100
        )

        if expense_ratio > 80:

            recommendations.append(
                "Your expenses consume more than 80% of your income. Focus on increasing savings."
            )

        elif expense_ratio < 50:

            recommendations.append(
                "Excellent financial discipline! Your expenses are well under control."
            )

    # =====================================
    # Final Response
    # =====================================

    return {
        "financial_health": financial_health,
        "recommendations": recommendations,
    }