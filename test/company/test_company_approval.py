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
