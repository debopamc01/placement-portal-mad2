from http import HTTPStatus

from flask import Blueprint, Response, request
from flask_login import login_required

from backend.models.company import Company
from backend.models.model_enums import (
    CompanyApprovalStatus,
    PlacementDriveStatus,
    UserRole,
    CompanyApprovalAction,
)
from backend.models.placement_drive import PlacementDrive
from backend.utils.decorators import role_required
from backend.utils.responses import error_response, success_response
from backend.extensions import db

admin_bp = Blueprint(name="admin", import_name=__name__, url_prefix="/api/admin")


def modify_company_approval_status(
    company_id: int, action: CompanyApprovalAction
) -> tuple[Response, HTTPStatus]:
    company = db.session.get(Company, company_id)
    if not company:
        return error_response(
            errors="Company does not exist", status=HTTPStatus.NOT_FOUND
        )

    if not isinstance(action, CompanyApprovalAction):
        return error_response(
            errors=f"Invalid action: {action}", status=HTTPStatus.BAD_REQUEST
        )

    if action == CompanyApprovalAction.APPROVE:
        company.approval_status = CompanyApprovalStatus.APPROVED

    else:
        if action == CompanyApprovalAction.REJECT:
            company.approval_status = CompanyApprovalStatus.REJECTED
        elif action == CompanyApprovalAction.BLACKLIST:
            company.approval_status = CompanyApprovalStatus.BLACKLISTED
        for drive in company.placement_drives:
            drive.status = PlacementDriveStatus.CLOSED

    try:
        db.session.commit()
        return success_response(
            data={"company_name": company.name, "status": company.approval_status.value}
        )
    except Exception as e:
        db.session.rollback()
        return error_response(errors=str(e), status=HTTPStatus.INTERNAL_SERVER_ERROR)


@login_required
@role_required(UserRole.ADMIN)
@admin_bp.post("/company/<int:company_id>/approve")
def approve_company(company_id: int):
    if not company_id:
        return error_response(
            errors="company_id is required",
            status=HTTPStatus.BAD_REQUEST,
        )
    return modify_company_approval_status(
        company_id=company_id, action=CompanyApprovalAction.APPROVE
    )


@login_required
@role_required(UserRole.ADMIN)
@admin_bp.post("/company/<int:company_id>/reject")
def reject_company(company_id: int):
    if not company_id:
        return error_response(
            errors="company_id is required",
            status=HTTPStatus.BAD_REQUEST,
        )
    return modify_company_approval_status(
        company_id=company_id, action=CompanyApprovalAction.REJECT
    )


@login_required
@role_required(UserRole.ADMIN)
@admin_bp.post("/company/<int:company_id>/blacklist")
def blacklist_company(company_id: int):
    if not company_id:
        return error_response(
            errors="company_id is required",
            status=HTTPStatus.BAD_REQUEST,
        )
    return modify_company_approval_status(
        company_id=company_id, action=CompanyApprovalAction.BLACKLIST
    )


@login_required
@role_required(UserRole.ADMIN)
@admin_bp.post("/placement-drives/<int:placement_drive_id>/approve")
def approve_placement_drive(placement_drive_id: int):
    placement_drive = db.session.scalar(
        db.select(PlacementDrive).where(
            PlacementDrive.id == placement_drive_id,
        )
    )
    if placement_drive is None:
        return error_response(
            errors="No placement drive found with the specified id",
            status=HTTPStatus.NOT_FOUND,
        )
    placement_drive.status = PlacementDriveStatus.ACTIVE
    try:
        db.session.commit()
        return success_response(
            data={
                "placement_drive_id": placement_drive.id,
                "status": placement_drive.status.value,
            }
        )
    except Exception as e:
        db.session.rollback()
        return error_response(errors=str(e), status=HTTPStatus.INTERNAL_SERVER_ERROR)


@login_required
@role_required(UserRole.ADMIN)
@admin_bp.post("/placement-drives/<int:placement_drive_id>/decline")
def decline_placement_drive(placement_drive_id: int):
    placement_drive = db.session.scalar(
        db.select(PlacementDrive).where(
            PlacementDrive.id == placement_drive_id,
        )
    )
    if placement_drive is None:
        return error_response(
            errors="No placement drive found with the specified id",
            status=HTTPStatus.NOT_FOUND,
        )
    placement_drive.status = PlacementDriveStatus.DECLINED
    try:
        db.session.commit()
        return success_response(
            data={
                "placement_drive_id": placement_drive.id,
                "status": placement_drive.status.value,
            }
        )
    except Exception as e:
        db.session.rollback()
        return error_response(errors=str(e), status=HTTPStatus.INTERNAL_SERVER_ERROR)


@admin_bp.get("/placement-drives")
@login_required
@role_required(UserRole.ADMIN)
def get_placement_drives():

    try:
        placement_drive_id = request.args.get("id")
        company_name = request.args.get("company_name")
        status = request.args.get("status")

        query = db.select(PlacementDrive)

        if placement_drive_id:
            query.where(PlacementDrive.id == int(placement_drive_id))
        if company_name:
            query.join(Company).where(Company.name.ilike(f"%{company_name}%"))
        if status:
            if not status in PlacementDriveStatus._value2member_map_:
                return error_response(
                    errors=f"Invalid status specified: {status}",
                    status=HTTPStatus.BAD_REQUEST,
                )
            query.where(PlacementDrive.status == PlacementDriveStatus(status))

        placement_drives = db.session.scalars(query).all()

        return success_response(
            data={"placement_drives": [drive.to_dict() for drive in placement_drives]}
        )
    except Exception as e:
        return error_response(errors=str(e), status=HTTPStatus.INTERNAL_SERVER_ERROR)
