"""
Сервис управления аутентификацией пользователей.

Функции:
- register_user: регистрация пользователей (первый становится `admin`)
- login_user: вход и выдача JWT-токена с ролью
- logout_user: выход с добавлением токена в `blacklist`
- is_token_blacklisted: проверка `blacklist`
"""

from typing import Tuple
from flask_jwt_extended import create_access_token, get_jwt
from datetime import timedelta
from app.utils.security import hash_password, verify_password
from app.repositories.user_repo import (
    get_user_by_username, get_user_by_email, create_user, get_all_users
)
from app.utils.redis_client import redis_client
from app.utils.response import create_response


def register_user(username: str, email: str, password: str, identity, role: str = "user") -> Tuple:
    """Регистрирует пользователя (первый — `admin`, остальные `user`, но `admin` может создать `admin`)."""

    if get_user_by_username(username):
        return create_response({"error": "Username already exists"}, 400)

    if get_user_by_email(email):
        return create_response({"error": "Email already registered"}, 400)

    # Первый пользователь — `admin`, остальные — `user` (или `admin`, если создаёт админ)
    if not get_all_users():
        role, identity = "admin", None

    user_role = get_jwt().get("role", "user") if identity else "admin"

    if identity and user_role != "admin" and role == "admin":
        return create_response({"error": "Only admin can create another admin"}, 403)

    create_user(username, email, hash_password(password), role)
    return create_response({"message": f"User registered successfully as {role}"}, 201)


def login_user(username: str, password: str) -> Tuple:
    """Вход пользователя с выдачей JWT-токена (включает роль пользователя в `claims`)."""
    if not (user := get_user_by_username(username)) or not verify_password(password, user.password_hash):
        return create_response({"error": "Invalid credentials"}, 401)

    return create_response({
        "access_token": create_access_token(
            identity=username,
            additional_claims={"role": user.role},
            expires_delta=timedelta(hours=1)
        )
    }, 200)


def logout_user() -> Tuple:
    """Добавляет токен в `blacklist`, что делает его недействительным."""
    redis_client.setex(f"blacklist:{get_jwt()['jti']}", 3600, "true")
    return create_response({"message": "Successfully logged out"}, 200)


def is_token_blacklisted(jti: str) -> bool:
    """Проверяет, есть ли токен в `blacklist`."""
    return redis_client.exists(f"blacklist:{jti}") > 0
