# Модели ответов сервиса администрирования.

from pydantic import BaseModel

from services.auth.models.responses import UserResponse
from services.common.models.responses import PaginatedResponse, PostResponse


class AdminStatsResponse(BaseModel):
    """GET /admin/stats — сводка дашборда."""

    total_users: int
    active_users: int
    total_posts: int
    total_comments: int
    total_conversations: int
    total_messages: int


AdminUserListResponse = PaginatedResponse[UserResponse]
AdminPostListResponse = PaginatedResponse[PostResponse]
