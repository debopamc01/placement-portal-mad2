from functools import wraps
from http import HTTPStatus
from flask import abort
from flask_login import current_user
from flask_login import login_required

def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        @login_required
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(HTTPStatus.UNAUTHORIZED)  # Unauthorized

            if current_user.role not in roles:
                abort(HTTPStatus.FORBIDDEN)  # Forbidden

            return fn(*args, **kwargs)
        return decorated_view
    return wrapper