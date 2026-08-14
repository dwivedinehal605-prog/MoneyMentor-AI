from io import BytesIO
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle,
)
from reportlab.lib.enums import TA_CENTER


def generate_pdf_report(
    report_data: dict,
):
    """
    Generate a professional financial report PDF.
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=10,
    )

    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=10,
        spaceAfter=20,
    )

    elements = []

    # =====================================
    # Title
    # =====================================

    elements.append(
        Paragraph(
            "MoneyMentor AI Financial Report",
            title_style,
        )
    )

    elements.append(
        Paragraph(
            f"Generated on: "
            f"{datetime.now().strftime('%d %B %Y, %I:%M %p')}",
            subtitle_style,
        )
    )

    # =====================================
    # Financial Summary
    # =====================================

    table_data = [
        ["Financial Metric", "Amount"],
        [
            "Total Income",
            f"INR {report_data.get('total_income', 0):,.2f}",
        ],
        [
            "Total Expense",
            f"INR {report_data.get('total_expense', 0):,.2f}",
        ],
        [
            "Savings",
            f"INR {report_data.get('savings', 0):,.2f}",
        ],
        [
            "Savings Rate",
            f"{report_data.get('savings_rate', 0):.2f}%",
        ],
    ]

    table = Table(
        table_data,
        colWidths=[250, 180],
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey,
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.black,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "FONTNAME",
                    (0, 1),
                    (-1, -1),
                    "Helvetica",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (1, -1),
                    "RIGHT",
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
            ]
        )
    )

    elements.append(table)

    elements.append(
        Spacer(1, 25)
    )

    # =====================================
    # Savings Status
    # =====================================

    savings = report_data.get(
        "savings",
        0,
    )

    if savings > 0:

        status = (
            "Financial Status: Positive Savings"
        )

    elif savings == 0:

        status = (
            "Financial Status: Break Even"
        )

    else:

        status = (
            "Financial Status: Deficit"
        )

    elements.append(
        Paragraph(
            status,
            styles["Heading3"],
        )
    )

    elements.append(
        Spacer(1, 10)
    )

    elements.append(
        Paragraph(
            "This report provides a summary of the "
            "income, expenses, savings and savings rate "
            "recorded in MoneyMentor AI.",
            styles["BodyText"],
        )
    )

    # =====================================
    # Build PDF
    # =====================================

    doc.build(elements)

    buffer.seek(0)

    return buffer