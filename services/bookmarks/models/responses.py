# Модели ответов сервиса закладок: список закладок — это список постов.

from services.common.models.responses import PaginatedResponse, PostResponse

BookmarkListResponse = PaginatedResponse[PostResponse]

__all__ = ["BookmarkListResponse", "PostResponse", "PaginatedResponse"]
