# Модели ответов сервиса пользователей.
# UserResponse переиспользуется из auth (та же схема бэкенда — дублировать нельзя),
# списки приходят в общем конверте PaginatedResponse.

from services.auth.models.responses import UserResponse
from services.common.models.responses import PaginatedResponse, PostResponse, UserBrief

UserListResponse = PaginatedResponse[UserBrief]
UserPostsResponse = PaginatedResponse[PostResponse]

__all__ = [
    "UserResponse",
    "UserBrief",
    "UserListResponse",
    "UserPostsResponse",
]
