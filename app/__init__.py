from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from app.routes.users import user_bp
        from app.routes.articles import article_bp
        from app.routes.auth import auth_bp

        app.register_blueprint(user_bp, url_prefix='/users')
        app.register_blueprint(article_bp, url_prefix='/articles')
        app.register_blueprint(auth_bp, url_prefix='/auth')

    @app.route('/')
    def home():
        return 'Hello, Flask is running'

    return app
