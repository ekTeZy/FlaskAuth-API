"""
Модуль аутентификации и авторизации пользователей.
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.auth_service import register_user, login_user, logout_user, is_token_blacklisted
from app.utils.response import create_response

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
@jwt_required(optional=True)
def register():
    """Регистрация пользователя (первый — `admin`, остальные `user`, но `admin` может создать `admin`)."""
    data = request.get_json()
    required_fields = ("username", "email", "password")

    if not all(field in data for field in required_fields):
        return create_response({"error": "All fields are required"}, 400)

    return register_user(**data, identity=get_jwt_identity())


@auth_bp.route("/login", methods=["POST"])
def login():
    """Авторизация пользователя."""
    data = request.get_json()
    if not all(field in data for field in ("username", "password")):
        return create_response({"error": "All fields are required"}, 400)

    return login_user(**data)


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """Выход пользователя."""
    return logout_user()


@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    """Пример защищённого маршрута (требуется токен)."""
    if is_token_blacklisted(get_jwt()["jti"]):
        return create_response({"error": "Token has been revoked"}, 401)

    return create_response({"message": f"Welcome, {get_jwt_identity()}!"})
