def test_create_article(client, create_user):
    user = create_user("editor", "editor@example.com", "password", role="editor")
    access_token = client.post('/auth/login', json={
        "email": "editor@example.com",
        "password": "password"
    }).json["access_token"]

    response = client.post('/articles/', json={
        "title": "Test Article",
        "content": "This is a test article."
    }, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 201
    assert response.json["message"] == "Article created successfully"


def test_get_articles(client, create_user, create_article):
    user = create_user("viewer", "viewer@example.com", "password", role="viewer")
    create_article("Sample Article", "Content", user.id)

    access_token = client.post('/auth/login', json={
        "email": "viewer@example.com",
        "password": "password"
    }).json["access_token"]

    response = client.get('/articles/', headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert len(response.json) > 0


def test_get_one_article(client, create_user, create_article):
    user = create_user("viewer", "viewer@example.com", "password", role="viewer")
    article = create_article("Sample Article", "Content", user.id)

    access_token = client.post('/auth/login', json={
        "email": "viewer@example.com",
        "password": "password"
    }).json["access_token"]

    response = client.get(f'/articles/{article.id}', headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json["id"] == article.id
    assert response.json["title"] == article.title


def test_update_article(client, create_user, create_article):
    user = create_user("editor", "editor@example.com", "password", role="editor")
    article = create_article("Old Title", "Old Content", user.id)

    access_token = client.post('/auth/login', json={
        "email": "editor@example.com",
        "password": "password"
    }).json["access_token"]

    response = client.put(f'/articles/{article.id}', json={
        "title": "Updated Title",
        "content": "Updated Content"
    }, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    assert response.json["message"] == "Article updated successfully"


def test_update_article_access_denied(client, create_user, create_article):
    user = create_user("regular_user", "user@example.com", "password", role="viewer")
    author = create_user("author_user", "author@example.com", "password", role="viewer")
    article = create_article("Original Title", "Original Content", author.id)

    access_token = client.post('/auth/login', json={
        "email": "user@example.com",
        "password": "password"
    }).json["access_token"]

    response = client.put(f'/articles/{article.id}', json={
        "title": "Updated Title",
        "content": "Updated Content"
    }, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 403
    assert response.json["message"] == "Access forbidden: you are not allowed to edit this article"


def test_delete_article(client, create_user, create_article):
    user = create_user("admin", "admin@example.com", "password", role="admin")
    article = create_article("Sample Article", "Content", user.id)

    access_token = client.post('/auth/login', json={
        "email": "admin@example.com",
        "password": "password"
    }).json["access_token"]

    response = client.delete(f'/articles/{article.id}', headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json["message"] == "Article deleted successfully"


def test_delete_article_unauthorized(client, create_user, create_article):
    user = create_user("viewer", "viewer@example.com", "password", role="viewer")
    article = create_article("Sample Article", "Content", user.id)

    response = client.delete(f'/articles/{article.id}')
    assert response.status_code == 401


def test_search_articles(client, create_user, create_article):
    user = create_user("viewer", "viewer@example.com", "password", role="viewer")
    create_article("Python Article", "Learning Python", user.id)
    create_article("Flask Article", "Building APIs", user.id)

    access_token = client.post('/auth/login', json={
        "email": "viewer@example.com",
        "password": "password"
    }).json["access_token"]

    response = client.get('/articles/search?q=Python', headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["title"] == "Python Article"
