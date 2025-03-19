"""
Модуль содержит определение модели Content для работы с контентом в базе данных.

Класс Content:
    - Представляет собой модель для хранения контента.
    - Содержит поля: id, title, body, created_at.
"""

from datetime import datetime
from app.database import db


class Content(db.Model):
    __tablename__ = "contents"

    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(255), nullable=False)
    body: str = db.Column(db.Text, nullable=False)
    created_at: datetime = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "created_at": self.created_at.isoformat()
        }

    def __repr__(self) -> str:
        return f"<Content {self.title}>"
