from datetime import datetime
from http import HTTPStatus
from zoneinfo import ZoneInfo

from flask import Blueprint, request
from flask_login import current_user, login_required

from backend.models.model_enums import CompanyApprovalStatus, UserRole
from backend.models.placement_drive import PlacementDrive
from backend.utils.decorators import role_required
from backend.utils.responses import error_response, success_response
from backend.extensions import db

company_bp = Blueprint("company", __name__, url_prefix="/api/company")


@company_bp.post("/placement-drives")
@login_required
@role_required(UserRole.COMPANY)
def create_placement_drive():
    if current_user.company.approval_status != CompanyApprovalStatus.APPROVED:
        return error_response(
            errors="Company is not yet approved", status=HTTPStatus.FORBIDDEN
        )

    data = request.get_json()

    title = data.get("job_title")
    description = data.get("description")
    eligibility_criteria = data.get("eligibility_criteria")
    application_deadline = data.get("application_deadline")

    if not title:
        return error_response(
            errors="job_title is required", status=HTTPStatus.BAD_REQUEST
        )

    try:
        new_drive = PlacementDrive()
        new_drive.job_title = title
        new_drive.job_description = description
        new_drive.eligibility_criteria = eligibility_criteria
        new_drive.application_deadline = (
            datetime.fromisoformat(application_deadline).astimezone(
                tz=ZoneInfo("Asia/Kolkata")
            )
            if application_deadline
            else None
        )
        new_drive.company = current_user.company
        db.session.add(new_drive)
        db.session.commit()
        return success_response(
            data={"placement_drive": new_drive.to_dict()}, status=HTTPStatus.CREATED
        )
    except Exception as e:
        db.session.rollback()
        return error_response(errors=str(e), status=HTTPStatus.INTERNAL_SERVER_ERROR)


@company_bp.get("/placement-drives")
@login_required
@role_required(UserRole.COMPANY)
def get_placement_drives():

    if current_user.company.approval_status != CompanyApprovalStatus.APPROVED:
        return error_response(
            errors="Company is not yet approved", status=HTTPStatus.FORBIDDEN
        )

    placement_drives = current_user.company.placement_drives
    return success_response(
        data={"placement_drives": [drive.to_dict() for drive in placement_drives]}
    )


@company_bp.get("/placement-drives/<int:drive_id>")
@login_required
@role_required(UserRole.COMPANY)
def get_placement_drive(drive_id: int):

    if current_user.company.approval_status != CompanyApprovalStatus.APPROVED:
        return error_response(
            errors="Company is not yet approved", status=HTTPStatus.FORBIDDEN
        )

    placement_drive = db.session.scalar(
        db.select(PlacementDrive).filter_by(
            id=drive_id,
            company_id=current_user.company.id,
        )
    )
    if placement_drive is None:
        return error_response(
            errors="Placement drive not found", status=HTTPStatus.NOT_FOUND
        )
    return success_response(data={"placement_drive": placement_drive.to_dict()})

#TODO: add PUT API for editing placement drive
