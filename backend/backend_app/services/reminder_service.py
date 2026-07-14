from datetime import datetime, timedelta, timezone
from typing import Sequence

from backend_app.extensions import db

from backend_app.models.placement_drive import PlacementDrive
from backend_app.models.model_enums import PlacementDriveStatus
from backend_app.models.student import Student

from backend_app.services.email_service import (
    send_deadline_reminder,
)

DAYS_BEFORE_DEADLINE_TO_REMIND = 2


def _application_deadline_to_datetime(application_deadline: str) -> datetime:

    return datetime.fromisoformat(application_deadline).astimezone(timezone.utc)


def send_placement_drive_daily_deadline_reminders():

    today = datetime.now(timezone.utc)

    date_after_n_days = today + timedelta(days=DAYS_BEFORE_DEADLINE_TO_REMIND)

    active_placement_drives: Sequence[PlacementDrive] = db.session.scalars(
        db.select(PlacementDrive).where(
            PlacementDrive.status == PlacementDriveStatus.ACTIVE,
        )
    ).all()

    valid_placement_drives = [
        pd
        for pd in active_placement_drives
        if today
        <= _application_deadline_to_datetime(pd.application_deadline)
        <= date_after_n_days
    ]

    students: Sequence[Student] = db.session.scalars(db.select(Student)).all()

    for student in students:

        applied_drive_ids = {
            application.placement_drive_id for application in student.applications
        }

        pending_drives = [
            drive
            for drive in valid_placement_drives
            if drive.id not in applied_drive_ids
        ]

        if pending_drives:
            send_deadline_reminder(
                student=student,
                placement_drives=pending_drives,
            )
