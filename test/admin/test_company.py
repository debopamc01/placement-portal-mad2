from datetime import datetime
from http import HTTPStatus

from config import ADMIN_EMAIL, ADMIN_PASSWORD


def test_approve_company(client):

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

    # Login as admin
    client.post(
        "/api/auth/login",
        json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD,
        },
    )
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


def test_reject_company(client):

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

    # Login as admin
    client.post(
        "/api/auth/login",
        json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD,
        },
    )
    # Reject the company
    response = client.post(f"/api/admin/company/{company_id}/reject")
    assert response.status_code == 200
    assert response.get_json().get("data").get("status") == "rejected"

    client.post(
        "/api/auth/logout",
    )

    # Verify the company is rejected

    response = client.post(
        "/api/auth/login",
        json={
            "email": "hr@acme.com",
            "password": "Password123",
        },
    )
    assert response.status_code == 403

    assert response.get_json().get("errors") == "Company registration has been rejected"


def test_blacklist_company(client):

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

    # Login as admin
    client.post(
        "/api/auth/login",
        json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD,
        },
    )
    # Blacklist the company
    response = client.post(f"/api/admin/company/{company_id}/blacklist")
    assert response.status_code == 200
    assert response.get_json().get("data").get("status") == "blacklisted"

    client.post(
        "/api/auth/logout",
    )

    # Verify the company is blacklisted

    response = client.post(
        "/api/auth/login",
        json={
            "email": "hr@acme.com",
            "password": "Password123",
        },
    )
    assert response.status_code == 403

    assert response.get_json().get("errors") == "Company has been blacklisted"


def test_get_placement_drives(client):

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

    # Login as admin
    client.post(
        "/api/auth/login",
        json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD,
        },
    )

    # Approve the company
    response = client.post(f"/api/admin/company/{company_id}/approve")
    assert response.status_code == 200

    client.post(
        "/api/auth/logout",
    )

    # Login as company
    response = client.post(
        "/api/auth/login", json={"email": "hr@acme.com", "password": "Password123"}
    )
    assert response.status_code == 200

    # Create a placement drive
    title = "Job Title 1"
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

    # Create another placement drive
    title = "Job Title 2"
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

    # Login as admin
    client.post(
        "/api/auth/login",
        json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD,
        },
    )

    # Get placement drives
    response = client.get("/api/admin/placement-drives")
    assert response.status_code == 200

    placement_drives = response.get_json().get("data").get("placement_drives")
    assert len(placement_drives) == 2

    # Get placement drives by id
    response = client.get("/api/admin/placement-drives?id=1")
    assert response.status_code == 200
    placement_drives = response.get_json().get("data").get("placement_drives")
    assert placement_drives[0].get("job_title") == "Job Title 1"

    # Get placement drives by company_name
    response = client.get("/api/admin/placement-drives?company-name=Acme")
    assert response.status_code == 200
    placement_drives = response.get_json().get("data").get("placement_drives")
    assert len(placement_drives) == 2
    assert placement_drives[0].get("company_id") == company_id

    # Get placement drives by status
    response = client.get("/api/admin/placement-drives?status=pending")
    assert response.status_code == 200
    placement_drives = response.get_json().get("data").get("placement_drives")
    assert len(placement_drives) == 2
    assert placement_drives[0].get("company_id") == company_id


def test_get_companies_success(client):
    # Register a company
    response = client.post(
        "/api/auth/register/company",
        json={
            "name": "Acme",
            "email": "hr@acme.com",
            "password": "Password123",
        },
    )
    assert response.status_code == HTTPStatus.CREATED

    # Register another company
    response = client.post(
        "/api/auth/register/company",
        json={
            "name": "Acme2",
            "email": "hr@acme2.com",
            "password": "Password123",
        },
    )
    assert response.status_code == 201

    # Login as admin
    client.post(
        "/api/auth/login",
        json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD,
        },
    )

    response = client.get("/api/admin/companies")

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()

    assert len(data["data"]["companies"]) == 2