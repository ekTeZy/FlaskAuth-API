"""
Репозиторий для работы с пользователями в базе данных.
"""
from typing import Optional, List
from app.database import db
from app.models.user import User


def get_user_by_username(username: str) -> Optional[User]:
    """Возвращает пользователя по `username` или None, если не найден."""
    return User.query.filter_by(username=username).first()


def get_user_by_email(email: str) -> Optional[User]:
    """Возвращает пользователя по `email` или None, если не найден."""
    return User.query.filter_by(email=email).first()


def create_user(username: str, email: str, password_hash: str, role: str) -> User:
    """Создаёт нового пользователя и сохраняет его в БД."""
    user = User(username=username, email=email,
                password_hash=password_hash, role=role)
    db.session.add(user)
    db.session.commit()
    return user


def get_all_users() -> List[User]:
    """Возвращает список всех пользователей."""
    return User.query.all()
