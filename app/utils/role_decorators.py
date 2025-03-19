from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        role = get_jwt().get("role")
        if role != "admin":
            return jsonify({"error": "Access denied"}), 403
        return func(*args, **kwargs)
    return wrapper
