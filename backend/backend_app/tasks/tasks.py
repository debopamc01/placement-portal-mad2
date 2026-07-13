from celery_app import celery

from backend_app.services.reminder_service import send_deadline_reminders

@celery.task
def send_reminders():
    send_deadline_reminders()