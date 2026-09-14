# Модели ответов сервиса комментариев.

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from services.common.models.responses import PaginatedResponse, UserBrief


class CommentResponse(BaseModel):
    """
    Комментарий или ответ на него.

    parent_comment_id заполнен у ответа. Собственного поля глубины бэкенд
    не отдаёт — ограничение в 3 уровня проверяется через цепочку ответов.
    """

    id: UUID
    post_id: UUID
    author: UserBrief
    content: str
    parent_comment_id: UUID | None = None
    is_deleted: bool = False
    likes_count: int = 0
    replies_count: int = 0
    created_at: datetime
    updated_at: datetime
    is_liked: bool = False


CommentListResponse = PaginatedResponse[CommentResponse]
