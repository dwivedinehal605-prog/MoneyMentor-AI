from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.dependencies.auth import (
    get_current_user,
)

from app.models.user import User

from app.schemas.report import (
    ReportSummaryResponse,
)

from app.services.report_service import (
    get_report_summary,
)

from fastapi.responses import StreamingResponse

from app.services.pdf_report_service import (
    generate_pdf_report,
)

from fastapi.responses import (
    StreamingResponse,
)

from app.services.csv_report_service import (
    generate_csv_report,
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.get(
    "/summary",
    response_model=ReportSummaryResponse,
)
def report_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Generate financial report summary.
    """

    return get_report_summary(
        db=db,
        user_id=current_user.id,
    )

@router.get(
    "/pdf",
)
def export_pdf_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Export financial report PDF.
    """

    report_data = (
        get_report_summary(
            db=db,
            user_id=current_user.id,
        )
    )

    pdf_file = (
        generate_pdf_report(
            report_data
        )
    )

    return StreamingResponse(
        pdf_file,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            "attachment; filename=financial_report.pdf"
        },
    )

@router.get(
    "/csv",
)
def export_csv_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Export financial report CSV.
    """

    report_data = (
        get_report_summary(
            db=db,
            user_id=current_user.id,
        )
    )

    csv_file = (
        generate_csv_report(
            report_data
        )
    )

    return StreamingResponse(
        iter(
            [csv_file.getvalue()]
        ),
        media_type="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=financial_report.csv"
        },
    )