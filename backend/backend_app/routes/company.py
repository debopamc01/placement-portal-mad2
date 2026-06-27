from datetime import datetime
from http import HTTPStatus
from zoneinfo import ZoneInfo

from flask import Blueprint, request
from flask_login import current_user, login_required

from backend_app.models.model_enums import (
    CompanyApprovalStatus,
    JobApplicationStatus,
    PlacementDriveStatus,
    UserRole,
)
from backend_app.models.placement_drive import PlacementDrive
from backend_app.utils.decorators import role_required
from backend_app.utils.responses import error_response, success_response
from backend_app.extensions import db

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

    if not all([title, description, eligibility_criteria, application_deadline]):
        return error_response(
            errors="All the fields are required", status=HTTPStatus.BAD_REQUEST
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

    placement_drives: list[PlacementDrive] = current_user.company.placement_drives
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
        db.select(PlacementDrive).where(
            PlacementDrive.id == drive_id,
            PlacementDrive.company_id == current_user.company.id,
        )
    )
    if placement_drive is None:
        return error_response(
            errors="Placement drive not found", status=HTTPStatus.NOT_FOUND
        )
    return success_response(data={"placement_drive": placement_drive.to_dict()})


@company_bp.patch("/placement-drives/<int:drive_id>")
@login_required
@role_required(UserRole.COMPANY)
def update_placement_drive(drive_id: int):
    if current_user.company.approval_status != CompanyApprovalStatus.APPROVED:
        return error_response(
            errors="Company is not yet approved", status=HTTPStatus.FORBIDDEN
        )

    placement_drive = db.session.scalar(
        db.select(PlacementDrive).where(
            PlacementDrive.id == drive_id,
            # Filter only those placement drives that belong to the company that is logged in
            PlacementDrive.company_id == current_user.company.id,
        )
    )

    if placement_drive is None:
        return error_response(
            errors="No placement drive found with the specified id",
            status=HTTPStatus.NOT_FOUND,
        )

    data = request.get_json()

    job_title = data.get("job_title")
    job_description = data.get("job_description")
    eligibility_criteria = data.get("eligibility_criteria")
    application_deadline = data.get("application_deadline")

    if not any(
        [job_title, job_description, eligibility_criteria, application_deadline]
    ):
        return error_response(
            errors="All fields are empty, placement drive not updated",
            status=HTTPStatus.BAD_REQUEST,
        )

    try:
        # Update only those fields that have been updated
        if job_title:
            placement_drive.job_title = job_title
        if job_description:
            placement_drive.job_description = job_description
        if eligibility_criteria:
            placement_drive.eligibility_criteria = eligibility_criteria
        if application_deadline:
            placement_drive.application_deadline = datetime.fromisoformat(
                application_deadline
            ).astimezone(tz=ZoneInfo("Asia/Kolkata"))

        # Updating placement drive resets placement drive status to pending
        placement_drive.status = PlacementDriveStatus.PENDING

        # Reset all the applications for the placement drive on update
        for application in placement_drive.applications:
            if not application.status == JobApplicationStatus.CLOSED:
                application.status = JobApplicationStatus.APPLIED

        db.session.commit()
        return success_response(
            data={"placement_drive": placement_drive.to_dict()}, status=HTTPStatus.OK
        )
    except Exception as e:
        db.session.rollback()
        return error_response(errors=str(e), status=HTTPStatus.INTERNAL_SERVER_ERROR)
