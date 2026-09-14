# Модели ответов сервиса постов.
# Сама карточка поста живёт в services/common (её отдают ещё search, bookmarks, admin).

from services.common.models.responses import HashtagResponse, PaginatedResponse, PostResponse

PostListResponse = PaginatedResponse[PostResponse]

__all__ = ["PostResponse", "PostListResponse", "HashtagResponse", "PaginatedResponse"]
