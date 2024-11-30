import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app import create_app, db
from app.models import User, Article
from werkzeug.security import generate_password_hash


def populate_db():
    app = create_app()
    with app.app_context():
        db.create_all()

        users = [
            User(username="admin_user", email="admin@example.com", password_hash=generate_password_hash("admin123"), role="admin"),
            User(username="editor_user", email="editor@example.com", password_hash=generate_password_hash("editor123"), role="editor"),
            User(username="viewer_user", email="viewer@example.com", password_hash=generate_password_hash("viewer123"), role="viewer"),
        ]

        articles = [
            Article(title="Admin Article", content="This is an article by admin.", author_id=1),
            Article(title="Editor Article", content="This is an article by editor.", author_id=2),
            Article(title="Viewer Article", content="This is an article by viewer.", author_id=3),
        ]

        db.session.add_all(users)
        db.session.add_all(articles)
        db.session.commit()
        print("Database populated successfully!")


if __name__ == "__main__":
    populate_db()
