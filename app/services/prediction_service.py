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
    Predict next month's total expense using
    historical monthly expense totals.

    Uses:
    - Average of available data when only a few
      months are available.
    - Linear Regression when sufficient historical
      monthly data is available.
    """

    if not expenses:
        return None

    # =====================================
    # Calculate Monthly Expense Totals
    # =====================================

    monthly_totals = defaultdict(float)

    for expense in expenses:

        if not expense.created_at:
            continue

        month = expense.created_at.strftime("%Y-%m")

        monthly_totals[month] += float(
            expense.amount
        )

    sorted_months = sorted(
        monthly_totals.keys()
    )

    totals = [
        monthly_totals[month]
        for month in sorted_months
    ]

    if not totals:
        return None

    # =====================================
    # One Month of Data
    # =====================================

    if len(totals) == 1:

        return round(
            float(totals[0]),
            2,
        )

    # =====================================
    # Two Months of Data
    # =====================================
    # With only two months, using linear
    # regression can create an unrealistic
    # prediction. Use the average instead.

    if len(totals) == 2:

        average_expense = sum(
            totals
        ) / len(totals)

        return round(
            float(average_expense),
            2,
        )

    # =====================================
    # Three or More Months
    # =====================================

    X = np.arange(
        len(totals),
        dtype=np.float64,
    ).reshape(-1, 1)

    y = np.array(
        totals,
        dtype=np.float64,
    )

    model = LinearRegression()

    model.fit(
        X,
        y,
    )

    next_month = np.array(
        [[len(totals)]],
        dtype=np.float64,
    )

    prediction = model.predict(
        next_month
    )

    predicted_amount = max(
        float(prediction[0]),
        0,
    )

    # =====================================
    # Prevent Extreme Predictions
    # =====================================

    average_expense = float(
        np.mean(totals)
    )

    maximum_reasonable_expense = (
        average_expense * 2
    )

    predicted_amount = min(
        predicted_amount,
        maximum_reasonable_expense,
    )

    return round(
        predicted_amount,
        2,
    )


def monthly_financial_forecast(
    db: Session,
    user_id: int,
):
    """
    Generate monthly financial forecast using
    income, expenses, budget and predicted
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

    total_income = float(
        total_income or 0
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

    # =====================================
    # Total Expense
    # =====================================

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

    total_expense = float(
        total_expense or 0
    )

    # =====================================
    # ML Prediction
    # =====================================

    predicted_expense = predict_monthly_expense(
        expenses
    )

    # If prediction cannot be generated,
    # use total expense as fallback.

    if predicted_expense is None:

        predicted_expense = total_expense

    predicted_expense = max(
        float(predicted_expense),
        0,
    )

    predicted_expense = round(
        predicted_expense,
        2,
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
        float(
            latest_budget.budget_amount
        )
        if latest_budget
        else 0.0
    )

    budget_amount = round(
        budget_amount,
        2,
    )

    # =====================================
    # Remaining Budget
    # =====================================

    remaining_budget = round(
        budget_amount
        - predicted_expense,
        2,
    )

    # =====================================
    # Predicted Savings
    # =====================================

    predicted_savings = round(
        total_income
        - predicted_expense,
        2,
    )

    # =====================================
    # Financial Health Score
    # =====================================

    financial_score = 100

    # No income
    if total_income == 0:

        financial_score -= 40

    # Predicted expense exceeds budget
    if (
        budget_amount > 0
        and predicted_expense > budget_amount
    ):

        financial_score -= 20

    # Predicted deficit
    if predicted_savings < 0:

        financial_score -= 20

    # High spending ratio
    if total_income > 0:

        expense_ratio = (
            total_expense
            / total_income
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

    if predicted_savings > 0:

        savings_status = (
            f"You are projected to save approximately "
            f"₹{predicted_savings:.2f} this month."
        )

    elif predicted_savings == 0:

        savings_status = (
            "You are projected to break even this month."
        )

    else:

        savings_status = (
            f"You are projected to have a deficit of "
            f"₹{abs(predicted_savings):.2f} this month."
        )

    # =====================================
    # Recommendations
    # =====================================

    recommendations = []

    if predicted_savings < 0:

        recommendations.append(
            "Reduce discretionary expenses to eliminate "
            "your projected monthly deficit."
        )

    if (
        budget_amount > 0
        and predicted_expense > budget_amount
    ):

        recommendations.append(
            "Your projected expenses exceed your monthly "
            "budget. Review your largest spending categories."
        )

    if total_income == 0:

        recommendations.append(
            "Add your income records to receive more "
            "accurate financial insights."
        )

    if (
        total_income > 0
        and predicted_savings > 0
    ):

        recommendations.append(
            "Consider investing a portion of your "
            "monthly savings."
        )

    if not recommendations:

        recommendations.append(
            "Excellent financial discipline. Continue "
            "monitoring your monthly finances."
        )

    # =====================================
    # Forecast Message
    # =====================================

    if total_income == 0:

        if budget_amount == 0:

            forecast = (
                "No income records or monthly budget found. "
                "Add your income and create a budget to "
                "receive accurate financial forecasts."
            )

        elif predicted_expense <= budget_amount:

            forecast = (
                "No income records found. Add your monthly "
                "income to receive accurate savings forecasts. "
                "Based on your current spending, you are "
                "expected to remain within your budget."
            )

        else:

            forecast = (
                "No income records found. Add your income to "
                "receive more accurate financial forecasts. "
                "Based on your current spending pattern, you "
                "may exceed your monthly budget."
            )

    else:

        if budget_amount == 0:

            forecast = (
                "No monthly budget has been set. Create a "
                "monthly budget to improve your financial planning."
            )

        elif predicted_expense <= budget_amount:

            forecast = (
                f"Excellent! Based on your current financial "
                f"trend, you are projected to stay within your "
                f"monthly budget with approximately "
                f"₹{remaining_budget:.2f} remaining."
            )

        else:

            over_budget = abs(
                remaining_budget
            )

            forecast = (
                f"Warning! You are projected to exceed your "
                f"monthly budget by approximately "
                f"₹{over_budget:.2f}. Consider reducing "
                f"non-essential expenses or increasing your income."
            )

    # =====================================
    # Final Response
    # =====================================

    return {
        "total_income": round(
            total_income,
            2,
        ),
        "total_expense": round(
            total_expense,
            2,
        ),
        "predicted_expense": round(
            predicted_expense,
            2,
        ),
        "predicted_savings": round(
            predicted_savings,
            2,
        ),
        "budget": budget_amount,
        "remaining_budget": remaining_budget,
        "financial_score": financial_score,
        "health_status": health_status,
        "savings_status": savings_status,
        "recommendations": recommendations,
        "forecast": forecast,
    }