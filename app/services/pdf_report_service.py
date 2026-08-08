from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)

from reportlab.lib.styles import (
    getSampleStyleSheet,
)


def generate_pdf_report(
    report_data: dict,
):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer
    )

    styles = (
        getSampleStyleSheet()
    )

    elements = []

    elements.append(
        Paragraph(
            "MoneyMentor AI Financial Report",
            styles["Title"],
        )
    )

    elements.append(
        Spacer(1, 12)
    )

    elements.append(
        Paragraph(
            f"Total Income: ₹{report_data['total_income']}",
            styles["BodyText"],
        )
    )

    elements.append(
        Paragraph(
            f"Total Expense: ₹{report_data['total_expense']}",
            styles["BodyText"],
        )
    )

    elements.append(
        Paragraph(
            f"Savings: ₹{report_data['savings']}",
            styles["BodyText"],
        )
    )

    elements.append(
        Paragraph(
            f"Savings Rate: {report_data['savings_rate']}%",
            styles["BodyText"],
        )
    )

    doc.build(
        elements
    )

    buffer.seek(0)

    return buffer