# Модели ответов сервиса уведомлений.

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from services.common.models.responses import PaginatedResponse, UserBrief


class NotificationResponse(BaseModel):
    """
    Уведомление.

    type        — like | comment | follow | follow_request | mention | message
    target_type — на что ссылается уведомление (post, comment, user);
                  конкретная сущность адресуется парой target_type + target_id
    """

    id: UUID
    actor: UserBrief | None = None
    type: str
    target_type: str | None = None
    target_id: UUID | None = None
    is_read: bool
    created_at: datetime


class UnreadCountResponse(BaseModel):
    """GET /notifications/unread-count."""

    count: int


NotificationListResponse = PaginatedResponse[NotificationResponse]
