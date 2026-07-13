from typing import Sequence

from flask import render_template
from flask_mail import Message

from backend_app.models.placement_drive import PlacementDrive
from backend_app.models.student import Student
from backend_app.extensions import mail
from flask import current_app


def send_deadline_reminder(
    student: Student, placement_drives: Sequence[PlacementDrive]
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
