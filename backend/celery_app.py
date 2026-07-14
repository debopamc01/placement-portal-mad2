from datetime import datetime, timedelta

from celery import Celery
from celery.schedules import crontab

from backend_app import create_backend_app

import tzlocal


def create_celery_app() -> Celery:

    flask_app = create_backend_app()

    celery = Celery(
        main=flask_app.name,
        broker="redis://localhost:6379/0",
        backend="redis://localhost:6379/1",
    )

    celery.conf.update(timezone=tzlocal.get_localzone_name(), enable_utc=False)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    return celery


celery = create_celery_app()

celery.autodiscover_tasks(packages=["backend_app.tasks"])


celery.conf.beat_schedule = {
    ########################
    # Task: Daily Reminder Email for placement drives: Runs every day at 9 am
    "daily_reminders": {
        "task": "backend_app.tasks.tasks.send_reminders",
        # "schedule": timedelta(minutes=1),
        "schedule": crontab(hour=9),
    },
    ########################
    # Task: Monthly report email for admin: Runs on 1st day of every month at 10 am
    "monthly_reports": {
        "task": "backend_app.tasks.tasks.send_monthly_reports",
        # "schedule": timedelta(minutes=1),
        "schedule": crontab(day_of_month=1, hour=10),
    },
}
