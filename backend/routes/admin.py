from http import HTTPStatus

from flask import Blueprint, Response
from flask_login import login_required

from backend.models.company import Company
from backend.models.model_enums import (
    CompanyApprovalStatus,
    PlacementDriveStatus,
    UserRole,
    CompanyApprovalAction,
)
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
