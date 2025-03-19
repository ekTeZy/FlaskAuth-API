"""
Репозиторий для работы с контентом в базе данных.
"""
from typing import List, Optional
from app.database import db
from app.models.content import Content


def get_all_content() -> List[Content]:
    """Возвращает все записи контента, отсортированные по убыванию даты создания."""
    return Content.query.order_by(Content.created_at.desc()).all()


def get_content_by_id(content_id: int) -> Optional[Content]:
    """Возвращает запись контента по ID или None, если не найдено."""
    return Content.query.get(content_id)


def create_content(title: str, body: str) -> Content:
    """Создаёт новую запись контента и сохраняет её в БД."""
    content = Content(title=title, body=body)
    db.session.add(content)
    db.session.commit()
    return content


def update_content(content_id: int, title: str, body: str) -> Optional[Content]:
    """Обновляет существующую запись контента, если она существует."""
    if content := get_content_by_id(content_id):
        content.title, content.body = title, body
        db.session.commit()
    return content


def delete_content(content_id: int) -> bool:
    """Удаляет запись контента, если она существует, и возвращает True/False."""
    if content := get_content_by_id(content_id):
        db.session.delete(content)
        db.session.commit()
        return True
    return False
