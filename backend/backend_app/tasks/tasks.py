from celery_app import celery

from backend_app.services.reminder_service import (
    send_placement_drive_daily_deadline_reminders,
)
from backend_app.services.monthly_report_service import send_monthly_reports_to_admin


@celery.task
def send_daily_reminders():
    send_placement_drive_daily_deadline_reminders()


@celery.task
def send_monthly_reports():
    send_monthly_reports_to_admin()
