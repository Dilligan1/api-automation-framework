# Модели запросов сервиса реакций.

from pydantic import BaseModel


class ReactionPayload(BaseModel):
    """Тип реакции при лайке поста или комментария."""

    reaction: str = "like"
