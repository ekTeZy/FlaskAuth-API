"""
Модуль для автоматического создания администратора при старте приложения.
"""

from app.database import db
from app.repositories.user_repo import get_user_by_username, create_user
from app.utils.security import hash_password
import logging 

DEFAULT_ADMIN = {
    "username": "admin",
    "email": "admin@example.com",
    "password": "adminpassword",
    "role": "admin"
}


def create_admin_if_not_exists():
    if not get_user_by_username(DEFAULT_ADMIN["username"]):
        hashed_password = hash_password(DEFAULT_ADMIN["password"])
        create_user(DEFAULT_ADMIN["username"], DEFAULT_ADMIN["email"],
                    hashed_password, DEFAULT_ADMIN["role"])
        logging.info("Admin created")
    else:
        logging.info("Admin is already exists")
