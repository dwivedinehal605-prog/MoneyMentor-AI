
from collections import defaultdict

from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.income import Income


def generate_recommendations(
    db: Session,
    user_id: int,
):
    """
    Generate personalized financial recommendations
    based on the user's income and expense behavior.
    """

    # --------------------------------
    # Fetch User Financial Data
    # --------------------------------

    incomes = (
        db.query(Income)
        .filter(
            Income.user_id == user_id
        )
        .all()
    )

    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == user_id
        )
        .all()
    )

    # --------------------------------
    # Calculate Totals
    # --------------------------------

    total_income = sum(
        income.amount
        for income in incomes
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

    # --------------------------------
    # Category Analysis
    # --------------------------------

    category_totals = defaultdict(float)

    for expense in expenses:
        category_totals[
            expense.category
        ] += expense.amount

    if category_totals:

        highest_spending_category = max(
            category_totals,
            key=category_totals.get,
        )

        highest_category_amount = (
            category_totals[
                highest_spending_category
            ]
        )

        category_percentage = (
            (
                highest_category_amount /
                total_expense
            ) * 100
            if total_expense > 0
            else 0
        )

    else:

        highest_spending_category = "N/A"
        category_percentage = 0

    # --------------------------------
    # Monthly Expense Trend
    # --------------------------------

    monthly_totals = defaultdict(float)

    for expense in expenses:

        month = expense.created_at.strftime(
            "%Y-%m"
        )

        monthly_totals[month] += (
            expense.amount
        )

    months = sorted(
        monthly_totals.keys()
    )

    if len(months) >= 2:

        previous_month_expense = (
            monthly_totals[months[-2]]
        )

        current_month_expense = (
            monthly_totals[months[-1]]
        )

        if (
            current_month_expense >
            previous_month_expense
        ):
            monthly_trend = "Increasing"

        elif (
            current_month_expense <
            previous_month_expense
        ):
            monthly_trend = "Decreasing"

        else:
            monthly_trend = "Stable"

    else:

        monthly_trend = (
            "Not enough monthly data"
        )

    # --------------------------------
    # No Income Scenario
    # --------------------------------

    if total_income <= 0:

        financial_health = (
            "No Income Data"
        )

        recommendations = [
            "Add income records to get personalized financial recommendations.",
            "Track your expenses regularly to understand your spending habits.",
            "Add a monthly income source to calculate your savings rate and financial health."
        ]

        return {
            "financial_health":
                financial_health,

            "recommendations":
                recommendations,
        }

    # --------------------------------
    # Negative Savings
    # --------------------------------

    if savings < 0:

        financial_health = "Poor"

        deficit = abs(savings)

        recommendations = [
            (
                f"Your expenses are ₹{deficit:.2f} "
                "higher than your income. Reduce "
                "non-essential spending immediately."
            ),

            (
                f"Review your '{highest_spending_category}' "
                "expenses and identify areas where you "
                "can cut costs."
            ),

            "Create a strict monthly budget to control your spending.",

            "Avoid unnecessary purchases until your expenses are below your income.",
        ]

        if monthly_trend == "Increasing":

            recommendations.append(
                "Your expenses are increasing. Monitor your spending closely this month."
            )

        return {
            "financial_health":
                financial_health,

            "recommendations":
                recommendations,
        }

    # --------------------------------
    # Very High Expense Ratio
    # --------------------------------

    expense_ratio = (
        total_expense /
        total_income
    ) * 100

    if expense_ratio > 90:

        financial_health = "Poor"

        recommendations = [
            "Your expenses consume more than 90% of your income.",

            (
                f"Reduce spending in your highest "
                f"category: '{highest_spending_category}'."
            ),

            "Create a strict monthly budget and set spending limits.",

            "Try to build an emergency savings fund.",
        ]

    # --------------------------------
    # High Expense Ratio
    # --------------------------------

    elif expense_ratio > 70:

        financial_health = "Average"

        recommendations = [
            (
                f"Your expenses consume approximately "
                f"{expense_ratio:.2f}% of your income."
            ),

            (
                f"Review your '{highest_spending_category}' "
                "expenses and look for ways to reduce them."
            ),

            "Try to increase your monthly savings rate.",

            "Set category-wise spending limits.",
        ]

    # --------------------------------
    # Healthy Financial Situation
    # --------------------------------

    else:

        financial_health = "Good"

        recommendations = [
            (
                f"Your current savings rate is "
                f"{savings_rate:.2f}%. Keep maintaining "
                "your spending discipline."
            ),

            (
                f"Your highest spending category is "
                f"'{highest_spending_category}'. "
                "Continue monitoring it regularly."
            ),

            "Consider investing a portion of your savings for long-term growth.",

            "Set long-term financial goals to strengthen your financial future.",
        ]

    # --------------------------------
    # Category Concentration Warning
    # --------------------------------

    if (
        total_expense > 0
        and category_percentage >= 40
    ):

        recommendations.append(
            (
                f"'{highest_spending_category}' represents "
                f"approximately {category_percentage:.2f}% "
                "of your total expenses. Consider reducing "
                "spending in this category."
            )
        )

    # --------------------------------
    # Increasing Spending Warning
    # --------------------------------

    if monthly_trend == "Increasing":

        recommendations.append(
            "Your expenses are increasing compared with the previous month. Monitor your spending trend."
        )

    elif monthly_trend == "Decreasing":

        recommendations.append(
            "Your expenses are decreasing compared with the previous month. Keep up the good work."
        )

    # --------------------------------
    # Final Response
    # --------------------------------

    return {
        "financial_health":
            financial_health,

        "recommendations":
            recommendations,
    }