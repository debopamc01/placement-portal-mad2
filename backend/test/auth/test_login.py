def test_company_registration(client):
    """
    Test successful company registration
    """

    response = client.post(
        "/api/auth/register/company",
        json={
            "name": "Acme Inc",
            "email": "hr@acme.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 201

def test_invalid_password(client):
    """
    Test student login with wrong password
    """

    client.post(
        "/api/auth/register/student",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "Password123",
        },
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": "john@example.com",
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401