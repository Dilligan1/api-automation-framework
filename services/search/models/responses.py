# Модели ответов поиска — переиспользуют общие карточки.

from services.common.models.responses import (
    HashtagResponse,
    PaginatedResponse,
    PostResponse,
    UserBrief,
)

UserSearchResponse = PaginatedResponse[UserBrief]
PostSearchResponse = PaginatedResponse[PostResponse]
HashtagSearchResponse = PaginatedResponse[HashtagResponse]

__all__ = [
    "UserSearchResponse",
    "PostSearchResponse",
    "HashtagSearchResponse",
    "HashtagResponse",
    "PaginatedResponse",
    "PostResponse",
    "UserBrief",
]
