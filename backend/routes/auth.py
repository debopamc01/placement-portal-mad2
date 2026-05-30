from flask import Blueprint, request
from flask_login import current_user, login_user, logout_user

from backend.models.user import User
from backend.utils.responses import *

auth_bp = Blueprint(name="auth", import_name=__name__, url_prefix="/api/auth")


@auth_bp.post("/login")
def login():
    """
    Log in user if provided credentials are correct.
    """

    data = request.get_json()

    if not data:
        return error_response(
            errors="Invalid JSON payload",
            status=HTTPStatus.BAD_REQUEST,
        )

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return error_response(
            errors="Email and password are required",
            status=HTTPStatus.BAD_REQUEST,
        )

    user = User.query.filter_by(email=email).first()

    if user is None:
        return error_response(
            errors="No user found with the specified email",
            status=HTTPStatus.NOT_FOUND,
        )

    if not user.check_password(password):
        return error_response(
            errors="Invalid password",
            status=HTTPStatus.UNAUTHORIZED,
        )

    status = login_user(user)

    if not status:
        return error_response(
            errors="Login error", status=HTTPStatus.INTERNAL_SERVER_ERROR
        )

    return success_response(
        message="Login successful",
        data={
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role,
            }
        },
    )


@auth_bp.get("/user")
def get_user():

    if not current_user.is_authenticated:
        return {"authenticated": False}, 401

    return {
        "authenticated": True,
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "role": current_user.role,
        },
    }

@auth_bp.post("/logout")
def logout():
    """
    Log out user
    """

    logout_user()

    return success_response(message="Logged out")