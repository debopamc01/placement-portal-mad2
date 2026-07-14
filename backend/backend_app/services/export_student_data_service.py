from datetime import datetime
from typing import Sequence

from flask_login import current_user

from backend_app.services.email_service import send_export_email
from backend_app.models.job_application import JobApplication
from backend_app.models.student import Student
from backend_app.extensions import db

from csv import DictWriter
import os
from config import BASE_DIR

CSV_EXPORT_FOLDER = os.path.join(BASE_DIR, "exports")
os.makedirs(CSV_EXPORT_FOLDER, exist_ok=True)


def export_student_data(student_id: int):
    current_student: Student | None = db.session.scalar(
        db.select(Student).where(Student.id == student_id)
    )

    if not current_student:
        return

    applications: Sequence[JobApplication] = db.session.scalars(
        db.select(JobApplication).where(JobApplication.student_id == student_id)
    ).all()

    data = [
        {
            "Student Id": student_id,
            "Student Name": current_student.name,
            "Company Name": application.placement_drive.company.name,
            "Job Title": application.placement_drive.job_title,
            "Application Status": application.status.upper(),
            "Application Date": datetime.fromisoformat(
                application.application_date
            ).astimezone().strftime("%d-%m-%Y %H:%M:%S"),
        }
        for application in applications
    ]

    headers = [
        "Student Id",
        "Student Name",
        "Company Name",
        "Job Title",
        "Application Status",
        "Application Date",
    ]
    csv_file_path = write_csv(student_id=student_id, headers=headers, rows=data)

    send_export_email(student=current_student, csv_file_path=csv_file_path)

    os.remove(csv_file_path)


def write_csv(student_id: int, headers: list[str], rows: list[dict]) -> str:
    file_path = os.path.join(
        CSV_EXPORT_FOLDER, f"student_{student_id}_applications.csv"
    )

    with open(file=file_path, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = DictWriter(csv_file, fieldnames=headers)

        writer.writeheader()
        writer.writerows(rows)

    return file_path
