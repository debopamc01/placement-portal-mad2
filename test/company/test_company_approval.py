from datetime import datetime

from backend.extensions import db
from backend.models.user import User
from backend.models.model_enums import (
    CompanyApprovalStatus,
)


def test_unapproved_company_cannot_login(client):

    client.post(
        "/api/auth/register/company",
        json={
            "name": "Acme",
            "email": "hr@acme.com",
            "password": "Password123",
        },
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": "hr@acme.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 403


def test_approved_company_can_login(app, client):

    client.post(
        "/api/auth/register/company",
        json={
            "name": "Acme",
            "email": "hr@acme.com",
            "password": "Password123",
        },
    )

    with app.app_context():

        user = db.session.scalar(db.select(User).where(User.email == "hr@acme.com"))

        user.company.approval_status = CompanyApprovalStatus.APPROVED

        db.session.commit()

    response = client.post(
        "/api/auth/login",
        json={
            "email": "hr@acme.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 200


def test_create_placement_drive(client):

    # Register a company
    response = client.post(
        "/api/auth/register/company",
        json={
            "name": "Acme",
            "email": "hr@acme.com",
            "password": "Password123",
        },
    )
    assert response.status_code == 201
    data = response.get_json().get("data")
    company_id = data.get("company").get("id")

    # Approve the company
    response = client.post(f"/api/admin/company/{company_id}/approve")
    assert response.status_code == 200

    client.post(
        "/api/auth/logout",
    )

    # Verify the company is approved
    # Company can login only if it is approved

    response = client.post(
        "/api/auth/login",
        json={
            "email": "hr@acme.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 200

    # Create a placement drive
    title = "Job Title"
    description = "Job Description"
    eligibility_criteria = "Eligibility Criteria"
    application_deadline = datetime.now().isoformat()

    response = client.post(
        "/api/company/placement-drives",
        json={
            "job_title": title,
            "description": description,
            "eligibility_criteria": eligibility_criteria,
            "application_deadline": application_deadline,
        },
    )

    assert response.status_code == 201
    data = response.get_json().get("data").get("placement_drive")
    expected_company_id = data.get("company_id")

    assert expected_company_id == company_id
