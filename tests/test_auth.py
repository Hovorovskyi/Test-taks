def test_register(client):
    response = client.post('/auth/register', json={
        "username": "test_user",
        "email": "test@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 201
    assert "access_token" in response.json
    assert "refresh_token" in response.json
    assert response.json["message"] == "User registered successfully"


def test_register_missing_fields(client):
    response = client.post('/auth/register', json={
        "username": "test_user"
    })
    assert response.status_code == 400
    assert response.json["message"] == "Missing request fields"


def test_register_invalid_email(client):
    response = client.post('/auth/register', json={
        "username": "test_user",
        "email": "invalid_email",
        "password": "securepassword"
    })
    assert response.status_code == 400
    assert response.json["message"] == "Invalid email address"


def test_login(client, create_user):
    create_user("test_user", "test@example.com", "securepassword")
    response = client.post('/auth/login', json={
        "email": "test@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json
    assert "refresh_token" in response.json
    assert response.json["message"] == "Login successful"


def test_login_invalid_credentials(client, create_user):
    create_user("test_user", "test@example.com", "securepassword")
    response = client.post('/auth/login', json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json["message"] == "Invalid email or password"


def test_refresh_token(client, create_user):
    create_user("test_user", "test@example.com", "securepassword")
    login_response = client.post('/auth/login', json={
        "email": "test@example.com",
        "password": "securepassword"
    })
    refresh_token = login_response.json["refresh_token"]

    response = client.post('/auth/refresh', headers={
        "Authorization": f"Bearer {refresh_token}"
    })
    assert response.status_code == 200
    assert "access_token" in response.json


def test_register_existing_email(client, create_user):
    create_user("test_user", "test@example.com", "securepassword")
    response = client.post('/auth/register', json={
        "username": "new_user",
        "email": "test@example.com",
        "password": "anotherpassword"
    })
    assert response.status_code == 400
    assert response.json["message"] == "Email already in use"
