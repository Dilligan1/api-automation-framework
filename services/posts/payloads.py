# Модели запросов сервиса постов.

from pydantic import BaseModel


class CreatePostPayload(BaseModel):
    """
    POST /posts.

    content    — 1..2000 символов
    visibility — public | followers_only
    """

    content: str
    image_url: str | None = None
    visibility: str = "public"


class UpdatePostPayload(BaseModel):
    """PATCH /posts/{id}. Доступен только автору и только 15 минут после создания."""

    content: str


class RepostPayload(BaseModel):
    """
    POST /posts/{id}/repost.

    repost_type — repost (без текста) | quote (с комментарием)
    """

    repost_type: str = "repost"
    content: str | None = None
