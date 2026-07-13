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

# Task: Daily Reminder Email for placement drives: Runs every day at 9 am
celery.conf.beat_schedule = {
    "daily-reminders": {
        "task": "backend_app.tasks.tasks.send_reminders",
        # "schedule": timedelta(minutes=1),
        "schedule": crontab(hour=9),
    },
}
