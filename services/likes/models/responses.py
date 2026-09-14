# Модели ответов сервиса реакций.

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from services.common.models.responses import PaginatedResponse, UserBrief


class LikeResponse(BaseModel):
    """Реакция. reaction: like | love | laugh | wow | sad | angry."""

    id: UUID
    user: UserBrief
    reaction: str
    created_at: datetime


LikeListResponse = PaginatedResponse[LikeResponse]
