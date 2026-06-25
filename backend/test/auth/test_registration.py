def test_student_registration(client):

    response = client.post(
        "/api/auth/register/student",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["success"] is True

def test_duplicate_email_registration(client):

    payload = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "Password123",
    }

    client.post(
        "/api/auth/register/student",
        json=payload,
    )

    response = client.post(
        "/api/auth/register/student",
        json=payload,
    )

    assert response.status_code == 409

def test_company_registration(client):

    response = client.post(
        "/api/auth/register/company",
        json={
            "name": "Acme Inc",
            "email": "hr@acme.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 201