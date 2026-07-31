from collections import defaultdict


def generate_dashboard_summary(incomes, expenses, insights):
    """
    Generate dashboard analytics for frontend.
    """

    # -------------------------------
    # Category-wise Analysis
    # -------------------------------

    category_totals = defaultdict(float)

    for expense in expenses:
        category_totals[expense.category] += expense.amount

    # -------------------------------
    # Top Categories
    # -------------------------------

    top_categories = sorted(
        [
            {
                "category": category,
                "amount": round(amount, 2),
            }
            for category, amount in category_totals.items()
        ],
        key=lambda x: x["amount"],
        reverse=True,
    )

    # -------------------------------
    # Category Distribution
    # -------------------------------

    total_expense = insights["total_expense"]

    category_distribution = []

    if total_expense > 0:
        for category, amount in category_totals.items():
            category_distribution.append(
                {
                    "category": category,
                    "percentage": round(
                        (amount / total_expense) * 100,
                        2,
                    ),
                }
            )

    # -------------------------------
    # Dashboard Statistics
    # -------------------------------

    total_transactions = len(expenses)

    total_categories = len(category_totals)

    average_expense = (
        insights["total_expense"] / len(expenses)
        if expenses
        else 0
    )

    average_income = (
        insights["total_income"] / len(incomes)
        if incomes
        else 0
    )

    # -------------------------------
    # Largest Expense
    # -------------------------------

    largest_expense = None

    if expenses:
        expense = max(
            expenses,
            key=lambda x: x.amount,
        )

        largest_expense = {
            "title": expense.title,
            "amount": expense.amount,
            "category": expense.category,
        }

    # -------------------------------
    # Recent Expenses
    # -------------------------------

    recent_expenses = sorted(
        expenses,
        key=lambda x: x.created_at,
        reverse=True,
    )[:5]

    recent_expenses = [
        {
            "title": expense.title,
            "amount": expense.amount,
            "category": expense.category,
        }
        for expense in recent_expenses
    ]

    # -------------------------------
    # Recent Incomes
    # -------------------------------

    recent_incomes = sorted(
        incomes,
        key=lambda x: x.created_at,
        reverse=True,
    )[:5]

    recent_incomes = [
        {
            "source": income.source,
            "amount": income.amount,
        }
        for income in recent_incomes
    ]

    # -------------------------------
    # Final Dashboard Response
    # -------------------------------

    return {
        "total_income": insights["total_income"],
        "total_expense": insights["total_expense"],
        "savings": insights["savings"],
        "savings_rate": insights["savings_rate"],

        "financial_health_score": insights["financial_health_score"],
        "health_status": insights["health_status"],

        "monthly_trend": insights["monthly_trend"],

        "total_transactions": total_transactions,
        "total_categories": total_categories,

        "average_expense": round(average_expense, 2),
        "average_income": round(average_income, 2),

        "largest_expense": largest_expense,

        "top_categories": top_categories,
        "category_distribution": category_distribution,

        "recent_expenses": recent_expenses,
        "recent_incomes": recent_incomes,
    }