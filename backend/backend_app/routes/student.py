from datetime import datetime
from http import HTTPStatus
from typing import Sequence
from zoneinfo import ZoneInfo

from flask import Blueprint, request
from flask_login import current_user, login_required

from backend_app.models.job_application import JobApplication
from backend_app.models.model_enums import PlacementDriveStatus, UserRole
from backend_app.models.placement_drive import PlacementDrive
from backend_app.utils.decorators import role_required
from backend_app.utils.responses import error_response, success_response
from backend_app.extensions import db

student_bp = Blueprint("student", __name__, url_prefix="/api/student")


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
        new_application.application_date = datetime.now().astimezone(
            ZoneInfo("Asia/Kolkata")
        )
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
