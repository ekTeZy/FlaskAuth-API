"""
Модуль, содержащий модель пользователя для базы данных.

Классы:
    User: Модель пользователя, представляющая таблицу "users" в базе данных.
"""

from app.database import db


class User(db.Model):
    __tablename__ = "users"

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(50), unique=True, nullable=False)
    email: str = db.Column(db.String(100), unique=True, nullable=False)
    password_hash: str = db.Column(db.String(255), nullable=False)
    role: str = db.Column(db.Enum("user", "admin", "moderator",
                          name="user_roles"), nullable=False, default="user")

    def __repr__(self) -> str:
        return f"<User {self.username}>"
