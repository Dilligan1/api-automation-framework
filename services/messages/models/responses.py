# Модели ответов сервиса диалогов.

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from services.common.models.responses import PaginatedResponse, UserBrief


class MessageResponse(BaseModel):
    """
    Сообщение.

    sender может быть null: у удалённого пользователя сообщения остаются
    в переписке без автора.
    """

    id: UUID
    conversation_id: UUID
    sender: UserBrief | None = None
    content: str
    image_url: str | None = None
    is_deleted: bool = False
    created_at: datetime


class ConversationResponse(BaseModel):
    """Диалог: 1:1 (is_group=false) или групповой."""

    id: UUID
    is_group: bool
    name: str | None = None
    participants: list[UserBrief] = []
    last_message: MessageResponse | None = None
    unread_count: int = 0
    created_at: datetime
    updated_at: datetime


ConversationListResponse = PaginatedResponse[ConversationResponse]
MessageListResponse = PaginatedResponse[MessageResponse]
