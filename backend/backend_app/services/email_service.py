from datetime import datetime
from typing import Sequence

from flask import render_template
from flask_mail import Message

from backend_app.services.types import PlacementDriveInfoForEmail
from backend_app.models.placement_drive import PlacementDrive
from backend_app.models.student import Student
from backend_app.extensions import mail
from flask import current_app
from config import ADMIN_EMAIL


def send_deadline_reminder(
    student: Student, placement_drives: Sequence[dict[str, str | datetime]]
):

    message = Message(
        subject="Placement Drive Deadline Reminder",
        recipients=[student.user.email],
        sender=current_app.config["MAIL_USERNAME"],
    )

    message.html = render_template(
        template_name_or_list="emails/deadline_reminder.html",
        student=student,
        placement_drives=placement_drives,
    )

    try:
        mail.send(message)
    except Exception as e:
        print(f"Exception while sending email to {student.user.email}:", str(e))


def send_monthly_report_email(
    month_str: str,
    placement_drive_reports: list[PlacementDriveInfoForEmail],
    total_applications: int,
    total_selected_applications: int,
):
    message = Message(
        subject=f"Monthly Report for Placement portal for {month_str}",
        recipients=[ADMIN_EMAIL],
        sender=current_app.config["MAIL_USERNAME"],
    )

    message.html = render_template(
        "emails/monthly_report.html",
        month=month_str,
        placement_drive_reports=placement_drive_reports,
        total_placement_drives=len(placement_drive_reports),
        total_applications=total_applications,
        total_selected_applications=total_selected_applications,
    )

    try:
        mail.send(message)
    except Exception as e:
        print(f"Exception while sending email to {ADMIN_EMAIL}:", str(e))
