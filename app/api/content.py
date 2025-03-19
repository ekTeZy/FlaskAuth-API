"""
Модуль управления контентом.
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.services.content_service import (
    get_all_content_service, get_content_service,
    create_content_service, update_content_service, delete_content_service
)
from app.utils.role_decorators import admin_required
from app.utils.response import create_response

content_bp = Blueprint("content", __name__, url_prefix="/content")


@content_bp.route("/", methods=["GET"])
@jwt_required()
def get_all_content():
    """Получение списка контента (доступно всем пользователям)."""
    return get_all_content_service()


@content_bp.route("/<int:content_id>", methods=["GET"])
@jwt_required()
def get_content(content_id: int):
    """Получение одного контента по ID."""
    return get_content_service(content_id)


@content_bp.route("/", methods=["POST"])
@jwt_required()
@admin_required
def create_content():
    """Создание контента (доступно только `admin`)."""
    data = request.get_json()
    if not all(field in data for field in ("title", "body")):
        return create_response({"error": "Title and body are required"}, 400)

    return create_content_service(**data)


@content_bp.route("/<int:content_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_content(content_id: int):
    """Обновление контента (доступно только `admin`)."""
    data = request.get_json()
    if not all(field in data for field in ("title", "body")):
        return create_response({"error": "Title and body are required"}, 400)

    return update_content_service(content_id, **data)


@content_bp.route("/<int:content_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_content(content_id: int):
    """Удаление контента (доступно только `admin`)."""
    return delete_content_service(content_id)
