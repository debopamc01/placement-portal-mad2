from backend_app import create_backend_app
from celery_utils.celery_app import celery

flask_app = create_backend_app()


class FlaskTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return self.run(*args, **kwargs)


celery.Task = FlaskTask

# Imports tasks AFTER Flask is ready, to avoid circular import during initialization
import backend_app.tasks.tasks
