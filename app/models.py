from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Text, CheckConstraint, ForeignKey


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    role = Column(
        String(20),
        nullable=False,
        default="viewer",
        server_default="viewer"
    )

    __table_args__ = (
        CheckConstraint("role IN ('admin', 'editor', 'viewer')", name="check_user_role"),
    )

    articles = relationship('Article', back_populates='author')

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


class Article(db.Model):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    author = relationship('User', back_populates='articles')

    def __repr__(self):
        return f'<Article {self.title} by {self.author.username}>'
