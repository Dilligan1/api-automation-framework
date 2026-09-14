# Модели запросов сервиса комментариев.

from pydantic import BaseModel


class CreateCommentPayload(BaseModel):
    """POST /posts/{post_id}/comments и POST /comments/{id}/replies."""

    content: str


class UpdateCommentPayload(BaseModel):
    """PATCH /comments/{id} — доступно автору комментария."""

    content: str
