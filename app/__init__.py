"""
Модуль инициализации приложения Flask.

Этот модуль содержит функцию create_app, которая создает и настраивает экземпляр приложения Flask.
Он также инициализирует расширения и регистрирует blueprints для различных частей приложения.

Используемые библиотеки:
- Flask
- Flask-JWT-Extended
- Flask-SQLAlchemy
- Flask-Migrate

Функции:
- create_app(): Создает и настраивает экземпляр приложения Flask.
"""

from flask import Flask
from flask_jwt_extended import JWTManager
from app.config import Config
from app.database import db, migrate
from app.api.auth import auth_bp
from app.api.content import content_bp

jwt = JWTManager()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(content_bp, url_prefix="/api/content")

    return app
