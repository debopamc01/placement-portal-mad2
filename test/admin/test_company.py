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
