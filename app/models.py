from app import db
import enum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Text, Enum, ForeignKey


class UserRole(enum.Enum):
    ADMIN = 'admin'
    EDITOR = 'editor'
    VIEWER = 'viewer'


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.VIEWER)

    articles = relationship('Article', back_populates='author')

    def __repr__(self):
        return f'<User {self.username} ({self.role.value})>'


class Article(db.Model):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    author = relationship('User', back_populates='articles')

    def __repr__(self):
        return f'<Article {self.title} by {self.author.username}>'
