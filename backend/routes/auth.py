from __future__ import annotations
from flask import Blueprint, request
from flask_login import current_user, login_user, logout_user

from backend.models.model_enums import UserRole
from backend.models.student import Student
from backend.models.user import User
from backend.utils.responses import *
from backend.extensions import db

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
            "user": user.to_dict()
        },
    )


@auth_bp.get("/user")
def get_user():

    if not current_user:
        return error_response(
            errors="No user is logged in",
            status=HTTPStatus.UNAUTHORIZED,
        )

    if not current_user.is_authenticated:
        return error_response(
            errors="User is not authenticated",
            status=HTTPStatus.UNAUTHORIZED,
        )

    return success_response(
        message="User exists",
        data={
            "user": current_user.to_dict()
        },
    )


@auth_bp.post("/logout")
def logout():
    """
    Log out user
    """

    logout_user()

    return success_response(message="Logged out")


@auth_bp.post("/register/student")
def register_student():
    """
    Register a new student
    """
    data = request.get_json()

    if not data:
        return error_response(
            errors="Invalid JSON payload",
            status=HTTPStatus.BAD_REQUEST,
        )
    user_name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not user_name or not email or not password:
        return error_response(
            errors="Name, email and password are required",
            status=HTTPStatus.BAD_REQUEST,
        )

    user = User.query.filter_by(email=email).first()

    if user:
        return error_response(
            errors="User with the specified email already exists",
            status=HTTPStatus.CONFLICT,
        )
    # TODO: add logic for email and password validation

    new_user = User()
    new_user.email = email
    new_user.set_password(password)
    new_user.role = UserRole.STUDENT

    new_student = Student()
    new_student.user = new_user

    try:
        db.session.add(new_user)
        db.session.add(new_student)
        db.session.commit()
        return success_response(
            message="Student registered successfully",
            data={
                "student": new_student.to_dict(),
            },
            status=HTTPStatus.CREATED,
        )
    except Exception as e:
        db.session.rollback()
        return error_response(
            errors="Error occurred while registering student",
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
