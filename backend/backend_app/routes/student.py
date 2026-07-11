from datetime import datetime, timezone
from http import HTTPStatus
import os
from typing import Sequence

from flask import Blueprint, request, send_from_directory
from flask_login import current_user, login_required

from backend_app.models.student import Student
from config import ALLOWED_RESUME_FILE_EXTENSIONS, UPLOAD_FOLDER_PATH
from backend_app.models.job_application import JobApplication
from backend_app.models.model_enums import PlacementDriveStatus, UserRole
from backend_app.models.placement_drive import PlacementDrive
from backend_app.utils.decorators import role_required
from backend_app.utils.responses import error_response, success_response
from backend_app.extensions import db
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

student_bp = Blueprint("student", __name__, url_prefix="/api/student")

STUDENT_RESUME_NAME_TEMPLATE = "Student_{user_id}.pdf"


@login_required
@role_required(UserRole.STUDENT)
@student_bp.post("/applications")
def apply_to_placement_drive():
    if current_user.student.blacklisted:
        return error_response(
            errors="Student is blacklisted", status=HTTPStatus.FORBIDDEN
        )
    data = request.get_json()
    placement_drive_id = data.get("placement_drive_id")
    application_time = data.get("application_time")

    placement_drive: PlacementDrive = db.session.scalar(
        db.select(PlacementDrive).where(PlacementDrive.id == placement_drive_id)
    )

    if not placement_drive:
        return error_response(
            errors="No placement drive with specified id", status=HTTPStatus.NOT_FOUND
        )

    if not placement_drive.status == PlacementDriveStatus.ACTIVE:
        return error_response(
            errors="Placement Drive is not active, can not apply",
            status=HTTPStatus.FORBIDDEN,
        )

    # TODO: Add logic for preventing applications after deadline

    application = db.session.scalar(
        db.select(JobApplication).where(
            JobApplication.student_id == current_user.student.id,
            JobApplication.placement_drive_id == placement_drive_id,
        )
    )
    if application:
        return error_response(
            errors="Duplicate application", status=HTTPStatus.CONFLICT
        )
    try:
        new_application = JobApplication()
        new_application.student = current_user.student
        new_application.placement_drive = placement_drive
        new_application.application_date = str(datetime.now(timezone.utc))
        db.session.add(new_application)
        db.session.commit()
        return success_response(
            data={"JobApplication": new_application.to_dict()},
            status=HTTPStatus.CREATED,
        )
    except Exception as e:
        db.session.rollback()
        return error_response(errors=str(e), status=HTTPStatus.INTERNAL_SERVER_ERROR)


@login_required
@role_required(UserRole.STUDENT)
@student_bp.get("/placement-drives")
def get_active_placement_drives():
    active_placement_drives: Sequence[PlacementDrive] = db.session.scalars(
        db.select(PlacementDrive).where(
            PlacementDrive.status == PlacementDriveStatus.ACTIVE
        )
    ).all()
    active_placement_drives_dicts = []
    for placement_drive in active_placement_drives:
        application: JobApplication | None = db.session.scalar(
            db.select(JobApplication).where(
                JobApplication.student_id == current_user.student.id,
                JobApplication.placement_drive_id == placement_drive.id,
            )
        )
        has_applied = application is not None
        application_status = application.status if has_applied else None
        placement_drive_dict = placement_drive.to_dict()
        placement_drive_dict["has_applied"] = has_applied
        placement_drive_dict["application_status"] = application_status
        active_placement_drives_dicts.append(placement_drive_dict)
    return success_response(data={"placement_drives": active_placement_drives_dicts})


@student_bp.get("/placement-drives/<int:drive_id>")
@login_required
@role_required(UserRole.STUDENT)
def get_placement_drive(drive_id: int):

    placement_drive: PlacementDrive | None = db.session.scalar(
        db.select(PlacementDrive).where(PlacementDrive.id == drive_id)
    )
    if placement_drive is None:
        return error_response(
            errors="Placement drive not found", status=HTTPStatus.NOT_FOUND
        )
    return success_response(data={"placement_drive": placement_drive.to_dict()})


allowed_mimetypes = {"pdf": "application/pdf"}


def valid_file(file: FileStorage) -> bool:
    filename = file.filename

    if not filename:
        return False

    if not "." in filename:
        return False

    extension = filename.rsplit(".")[-1].lower()
    return (
        extension in ALLOWED_RESUME_FILE_EXTENSIONS
        and file.mimetype == allowed_mimetypes[extension]
    )


@student_bp.post("/resume")
@login_required
@role_required(UserRole.STUDENT)
def upload_resume():

    try:
        if "resume" not in request.files:
            return error_response(
                errors="Resume not uploaded",
                status=HTTPStatus.BAD_REQUEST,
            )

        file = request.files.get("resume")

        if not file or not file.filename:
            return error_response(
                errors="No file selected",
                status=HTTPStatus.BAD_REQUEST,
            )

        if not valid_file(file):
            return error_response(
                errors="Unsupported file type",
                status=HTTPStatus.BAD_REQUEST,
            )

        storage_filename = STUDENT_RESUME_NAME_TEMPLATE.format(
            user_id=current_user.student.id
        )

        filepath = os.path.join(UPLOAD_FOLDER_PATH, storage_filename)

        file.save(filepath)

        current_user.student.resume_filename = secure_filename(file.filename)

        db.session.commit()

        return success_response(
            data={"resume_filename": current_user.student.resume_filename}
        )

    except Exception as e:
        db.session.rollback()
        return error_response(errors=str(e), status=HTTPStatus.INTERNAL_SERVER_ERROR)


@student_bp.get("/resume")
@login_required
@role_required(UserRole.STUDENT)
def download_resume():

    if current_user.student.resume_filename is None:
        return error_response(
            errors="Resume not available",
            status=HTTPStatus.NOT_FOUND,
        )

    storage_filename = STUDENT_RESUME_NAME_TEMPLATE.format(
        user_id=current_user.student.id
    )

    return send_from_directory(
        directory=UPLOAD_FOLDER_PATH,
        path=storage_filename,
        download_name=current_user.student.resume_filename,
    )


@student_bp.get("/profile")
@login_required
@role_required(UserRole.STUDENT)
def get_profile():
    student: Student = current_user.student

    return success_response(data={"student": student.to_dict()})


@student_bp.patch("/profile")
@login_required
@role_required(UserRole.STUDENT)
def update_profile():
    data = request.get_json()

    name = data.get("name")
    resume_filename = data.get("resume_filename")
    description = data.get("description")

    try:
        student: Student | None = current_user.student
        if not student:
            return error_response(
                errors="Student not found", status=HTTPStatus.NOT_FOUND
            )
        student.name = name
        student.resume_filename = resume_filename
        student.description = description
        db.session.commit()
        return success_response(data={"student": student.to_dict()})
    except Exception as e:
        db.session.rollback()
        return error_response(errors=str(e), status=HTTPStatus.INTERNAL_SERVER_ERROR)
