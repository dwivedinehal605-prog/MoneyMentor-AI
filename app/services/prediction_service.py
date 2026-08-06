from collections import defaultdict

import numpy as np
from sklearn.linear_model import LinearRegression
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.models.expense import Expense
from app.models.income import Income


def predict_monthly_expense(expenses):
    """
    Predict the next month's
    total expense using
    historical monthly totals.
    """

    if len(expenses) < 2:
        return None

    monthly_totals = defaultdict(float)

    for expense in expenses:

        month = expense.created_at.strftime(
            "%Y-%m"
        )

        monthly_totals[month] += expense.amount

    sorted_months = sorted(
        monthly_totals.keys()
    )

    totals = [
        monthly_totals[month]
        for month in sorted_months
    ]

    if len(totals) < 2:
        return None

    X = np.arange(
        len(totals),
        dtype=np.float64,
    ).reshape(-1, 1)

    y = np.array(
        totals,
        dtype=np.float64,
    )

    model = LinearRegression()
    model.fit(X, y)

    next_month = np.array(
        [[len(totals)]],
        dtype=np.float64,
    )

    prediction = model.predict(
        next_month
    )

    return round(
        float(prediction[0]),
        2,
    )

def monthly_financial_forecast(
    db: Session,
    user_id: int,
):
    """
    Generate a monthly financial forecast
    based on the user's income,
    expenses, budget, and predicted
    future spending.
    """

    # =====================================
    # Total Income
    # =====================================

    total_income = (
        db.query(
            func.coalesce(
                func.sum(Income.amount),
                0,
            )
        )
        .filter(
            Income.user_id == user_id
        )
        .scalar()
    )

    # =====================================
    # Expense Records
    # =====================================

    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == user_id
        )
        .order_by(
            Expense.created_at.asc()
        )
        .all()
    )

    total_expense = (
        db.query(
            func.coalesce(
                func.sum(Expense.amount),
                0,
            )
        )
        .filter(
            Expense.user_id == user_id
        )
        .scalar()
    )

    # =====================================
    # Machine Learning Prediction
    # =====================================

    predicted_expense = predict_monthly_expense(
        expenses
    )

    if predicted_expense is None:
        predicted_expense = total_expense

    predicted_expense = max(
        predicted_expense,
        0,
    )

    # =====================================
    # Latest Budget
    # =====================================

    latest_budget = (
        db.query(Budget)
        .filter(
            Budget.user_id == user_id
        )
        .order_by(
            Budget.year.desc(),
            Budget.month.desc(),
        )
        .first()
    )

    budget_amount = (
        latest_budget.budget_amount
        if latest_budget
        else 0
    )

    budget_amount = round(
        budget_amount,
        2,
    )

    remaining_budget = round(
        budget_amount -
        predicted_expense,
        2,
    )

    predicted_savings = round(
        total_income -
        predicted_expense,
        2,
    )

    # =====================================
    # Financial Health Score
    # =====================================
    # Starting with a perfect financial score
    financial_score = 100

    # Penalize if no income is recorded
    if total_income == 0:
        financial_score -= 40

    # Penalize if predicted expenses exceed budget
    if (
        budget_amount > 0
        and predicted_expense > budget_amount
    ):
        financial_score -= 20

    # Penalize if there is a deficit
    if predicted_savings < 0:
        financial_score -= 20

    # Penalize if more than 80% of income is spent
    if total_income > 0:

        expense_ratio = (
            total_expense /
            total_income
        )

        if expense_ratio > 0.80:
            financial_score -= 20

    financial_score = max(
        0,
        min(
            financial_score,
            100,
        ),
    )

    # =====================================
    # Health Status
    # =====================================

    if financial_score >= 80:

        health_status = "Excellent"

    elif financial_score >= 60:

        health_status = "Good"

    elif financial_score >= 40:

        health_status = "Average"

    else:

        health_status = "Needs Improvement"

    # =====================================
    # Savings Status
    # =====================================

    recommendations = []

    if predicted_savings < 0:
       recommendations.append(
           "Reduce discretionary expenses to eliminate your projected monthly deficit."
        )

    if budget_amount > 0 and predicted_expense > budget_amount:
        recommendations.append(
            "Your projected expenses exceed your monthly budget. Review your largest spending categories."
       )

    if total_income == 0:
        recommendations.append(
            "Add your income records to receive more accurate financial insights."
        )

    if (
        total_income > 0
        and predicted_savings > 0
    ):
        recommendations.append(
            "Consider investing a portion of your monthly savings."
       )

    if len(recommendations) == 0:
        recommendations.append(
            "Excellent financial discipline. Continue monitoring your monthly finances."
       )

    # =====================================
    # Forecast Message
    # =====================================

    if total_income == 0:

        if budget_amount == 0:

            forecast = (
                "No income records or "
                "monthly budget found. "
                "Add your income and "
                "create a budget to "
                "receive accurate "
                "financial forecasts."
            )

        elif predicted_expense <= budget_amount:

            forecast = (
                "No income records found. "
                "Add your monthly income "
                "to receive accurate "
                "savings forecasts. "
                "Based on your current "
                "spending, you are "
                "expected to remain "
                "within your budget."
            )

        else:

            forecast = (
                "No income records found. "
                "Add your income to "
                "receive more accurate "
                "financial forecasts. "
                "Based on your current "
                "spending pattern, you "
                "may exceed your "
                "monthly budget."
            )

    else:

        if budget_amount == 0:

            forecast = (
                "No monthly budget has "
                "been set. Create a "
                "monthly budget to "
                "improve your financial "
                "planning."
            )

        elif predicted_expense <= budget_amount:

            forecast = (
                f"Excellent! Based on your current financial trend, "
                f"you are projected to stay within your monthly budget "
                f"with approximately ₹{remaining_budget:.2f} remaining."
         )

        else:

            over_budget = abs(
                remaining_budget
            )

            forecast = (
                f"Warning! You are "
                f"projected to exceed "
                f"your monthly budget by "
                f"approximately "
                f"₹{over_budget:.2f}. "
                f"Consider reducing "
                f"non-essential expenses "
                f"or increasing your "
                f"income."
            )

    # =====================================
    # Response
    # =====================================

    return {
        # Financial Summary
        "total_income": round(
            total_income,
            2,
        ),
        "total_expense": round(
            total_expense,
            2,
        ),

        # Predictions
        "predicted_expense": predicted_expense,
        "predicted_savings": predicted_savings,

        # Budget
        "budget": budget_amount,
        "remaining_budget": remaining_budget,

        # Health
        "financial_score": financial_score,
        "health_status": health_status,

        # Insights
        "savings_status": savings_status,
        "recommendations": recommendations,
        "forecast": forecast,
    }