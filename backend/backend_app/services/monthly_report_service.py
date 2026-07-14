from datetime import datetime, timedelta, timezone
from typing import Sequence


from backend_app.services.email_service import send_monthly_report_email
from backend_app.models.model_enums import JobApplicationStatus
from backend_app.models.placement_drive import PlacementDrive
from backend_app.extensions import db
from backend_app.services.types import PlacementDriveInfoForEmail


def send_monthly_reports_to_admin():
    last_day_of_last_month = datetime.now(timezone.utc) - timedelta(days=1)
    # This is to be run on 1st day of new month so 1 day offset is last day of last month

    last_month_str = last_day_of_last_month.strftime("%B %Y")

    all_placement_drives: Sequence[PlacementDrive] = db.session.scalars(
        db.select(PlacementDrive)
    ).all()

    placement_drives_last_month = [
        placement_drive
        for placement_drive in all_placement_drives
        if datetime.fromisoformat(placement_drive.created_at)
        .astimezone(timezone.utc)
        .month
        == last_day_of_last_month.month
    ]

    placement_drive_reports: list[PlacementDriveInfoForEmail] = [
        {
            "title": drive.job_title,
            "company": drive.company.name,
            "total_applications": len(drive.applications),
            "selected_applications": sum(
                application.status == JobApplicationStatus.SELECTED
                for application in drive.applications
            ),
        }
        for drive in placement_drives_last_month
    ]

    total_applications = sum(
        [
            pd["total_applications"]
            for pd in placement_drive_reports
            if isinstance(pd["total_applications"], int)
        ]
    )
    total_selected_applications = sum(
        [
            pd["selected_applications"]
            for pd in placement_drive_reports
            if isinstance(pd["selected_applications"], int)
        ]
    )

    send_monthly_report_email(
        month_str=last_month_str,
        placement_drive_reports=placement_drive_reports,
        total_applications=total_applications,
        total_selected_applications=total_selected_applications,
    )
