"""
Сервис управления контентом.

Функции:
- get_all_content_service: возвращает весь контент
- get_content_service: получает один объект контента
- create_content_service: создаёт новый контент
- update_content_service: обновляет контент
- delete_content_service: удаляет контент
"""

from typing import Tuple, Dict
from app.repositories.content_repo import (
    get_all_content, get_content_by_id, create_content, update_content, delete_content
)
from app.utils.response import create_response


def get_all_content_service() -> Tuple[Dict, int]:
    """Возвращает список всего контента."""
    return create_response({"content": [c.as_dict() for c in get_all_content()]}, 200)


def get_content_service(content_id: int) -> Tuple[Dict, int]:
    """Возвращает объект контента по ID или 404, если не найден."""
    return create_response(content.as_dict(), 200) if (content := get_content_by_id(content_id)) \
        else create_response({"error": "Content not found"}, 404)


def create_content_service(title: str, body: str) -> Tuple[Dict, int]:
    """Создаёт контент и возвращает его с `201`."""
    return create_response({
        "message": "Content created",
        "content": create_content(title, body).as_dict()
    }, 201)


def update_content_service(content_id: int, title: str, body: str) -> Tuple[Dict, int]:
    """Обновляет контент и возвращает обновлённые данные или `404`, если не найден."""
    content = update_content(content_id, title, body)
    if not content:
        return create_response({"error": "Content not found"}, 404)

    return create_response({
        "message": "Content updated",
        "content": content.as_dict()
    }, 200)


def delete_content_service(content_id: int) -> Tuple[Dict, int]:
    """Удаляет контент или возвращает `404`, если не найден."""
    return create_response({"message": "Content deleted"}, 200) if delete_content(content_id) \
        else create_response({"error": "Content not found"}, 404)
