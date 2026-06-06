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
