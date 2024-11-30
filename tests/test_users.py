def test_get_users(client, create_user):
    create_user("admin", "admin@example.com", "password", role="admin")
    create_user("editor", "editor@example.com", "password", role="editor")

    access_token = client.post('/auth/login', json={
        "email": "admin@example.com",
        "password": "password"
    }).json["access_token"]

    response = client.get('/users/', headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert len(response.json) >= 2


def test_get_user_by_id(client, create_user):
    admin_user = create_user("admin", "admin@example.com", "password", role="admin")
    access_token = client.post('/auth/login', json={
        "email": "admin@example.com",
        "password": "password"
    }).json["access_token"]

    response = client.get(f'/users/{admin_user.id}', headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json["username"] == "admin"
    assert response.json["email"] == "admin@example.com"


def test_create_user(client, create_user):
    create_user("admin", "admin@example.com", "password", role="admin")
    access_token = client.post('/auth/login', json={
        "email": "admin@example.com",
        "password": "password"
    }).json["access_token"]

    response = client.post('/users/', json={
        "username": "new_user",
        "email": "new_user@example.com",
        "password": "password",
        "role": "viewer"
    }, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 201
    assert response.json["message"] == "User created"


def test_update_user(client, create_user):
    admin_user = create_user("admin", "admin@example.com", "password", role="admin")
    target_user = create_user("target_user", "target@example.com", "password", role="viewer")
    access_token = client.post('/auth/login', json={
        "email": "admin@example.com",
        "password": "password"
    }).json["access_token"]

    response = client.put(f'/users/{target_user.id}', json={
        "username": "updated_user",
        "role": "editor"
    }, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    assert response.json["message"] == "User updated"


def test_delete_user(client, create_user):
    admin_user = create_user("admin", "admin@example.com", "password", role="admin")
    target_user = create_user("target_user", "target@example.com", "password", role="viewer")
    access_token = client.post('/auth/login', json={
        "email": "admin@example.com",
        "password": "password"
    }).json["access_token"]

    response = client.delete(f'/users/{target_user.id}', headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json["message"] == "User deleted"


def test_search_users(client, create_user):
    create_user("admin", "admin@example.com", "password", role="admin")
    create_user("editor", "editor_user@example.com", "password", role="editor")
    access_token = client.post('/auth/login', json={
        "email": "admin@example.com",
        "password": "password"
    }).json["access_token"]

    response = client.get('/users/search?q=editor', headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["username"] == "editor"
