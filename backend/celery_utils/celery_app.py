from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

import tzlocal


def create_celery_app() -> Celery:

    celery = Celery(
        main="placement_portal",
        broker="redis://localhost:6379/0",
        backend="redis://localhost:6379/1",
    )

    celery.conf.update(timezone=tzlocal.get_localzone_name(), enable_utc=False)

    return celery


celery = create_celery_app()

celery.autodiscover_tasks(packages=["backend_app.tasks"])


celery.conf.beat_schedule = {

    ########################
    # Task: Daily Reminder Email for placement drives: Runs every day at 9 am
    "daily_reminders": {
        "task": "backend_app.tasks.tasks.send_daily_deadline_reminders_task",
        # "schedule": timedelta(minutes=1),
        "schedule": crontab(hour=9),
    },

    ########################
    # Task: Monthly report email for admin: Runs on 1st day of every month at 10 am
    "monthly_reports": {
        "task": "backend_app.tasks.tasks.send_monthly_reports_task",
        # "schedule": timedelta(minutes=1),
        "schedule": crontab(day_of_month=1, hour=10),
    },
}
