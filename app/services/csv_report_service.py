from io import StringIO
import csv


def generate_csv_report(
    report_data: dict,
):
    output = StringIO()

    writer = csv.writer(
        output
    )

    writer.writerow(
        [
            "Metric",
            "Value",
        ]
    )

    writer.writerow(
        [
            "Total Income",
            report_data[
                "total_income"
            ],
        ]
    )

    writer.writerow(
        [
            "Total Expense",
            report_data[
                "total_expense"
            ],
        ]
    )

    writer.writerow(
        [
            "Savings",
            report_data[
                "savings"
            ],
        ]
    )

    writer.writerow(
        [
            "Savings Rate",
            report_data[
                "savings_rate"
            ],
        ]
    )

    output.seek(0)

    return output