from celery_utils.celery_app import celery

from backend_app.services.reminder_service import (
    send_placement_drive_daily_deadline_reminders,
)
from backend_app.services.monthly_report_service import send_monthly_reports_to_admin
from backend_app.services.export_student_data_service import export_student_data


@celery.task
def send_daily_deadline_reminders_task():
    send_placement_drive_daily_deadline_reminders()


@celery.task
def send_monthly_reports_task():
    send_monthly_reports_to_admin()


@celery.task
def export_student_applications_task(student_id: int):
    export_student_data(student_id=student_id)
