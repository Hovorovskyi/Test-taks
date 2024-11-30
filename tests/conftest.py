import pytest
from app import create_app, db
from app.models import User, Article


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": "test_secret",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def create_user():
    def _create_user(username, email, password, role="viewer"):
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
    return _create_user


@pytest.fixture
def create_article():
    def _create_article(title, content, author_id):
        article = Article(title=title, content=content, author_id=author_id)
        db.session.add(article)
        db.session.commit()
        return article
    return _create_article
