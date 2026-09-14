# Модели запросов сервиса диалогов.

from uuid import UUID

from pydantic import BaseModel


class CreateConversationPayload(BaseModel):
    """
    POST /conversations.

    Участники передаются идентификаторами, а не хэндлами: id берётся
    из каталога пользователей (GET /users) или из карточки профиля.
    """

    participant_ids: list[UUID]
    is_group: bool = False
    name: str | None = None  # имя группового чата, до 100 символов


class SendMessagePayload(BaseModel):
    """POST /conversations/{id}/messages. content — 1..2000 символов."""

    content: str
    image_url: str | None = None
