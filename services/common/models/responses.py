# Общие Pydantic-модели, переиспользуемые несколькими сервисами.
# Бэкенд отдаёт единый конверт пагинации и краткую карточку пользователя —
# дублировать их в каждом сервисе нет смысла.

from datetime import datetime
from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Конверт пагинации: GET-списки всех сервисов отдают именно его."""

    items: list[T]
    total: int
    page: int
    per_page: int
    pages: int


class UserBrief(BaseModel):
    """Краткая карточка пользователя — автор поста, участник диалога, подписчик."""

    id: UUID
    username: str
    display_name: str
    avatar_url: str | None = None
    is_verified: bool


class HashtagResponse(BaseModel):
    id: UUID
    name: str
    posts_count: int


class PostResponse(BaseModel):
    """Пост. Общая модель: возвращается из posts, search, bookmarks и admin."""

    id: UUID
    author: UserBrief
    content: str
    image_url: str | None = None
    is_pinned: bool
    is_deleted: bool
    parent_id: UUID | None = None
    repost_type: str | None = None
    visibility: str
    likes_count: int
    comments_count: int
    reposts_count: int
    hashtags: list[HashtagResponse] = []
    created_at: datetime
    updated_at: datetime
    is_liked: bool = False
    is_bookmarked: bool = False
    user_reaction: str | None = None


class ErrorResponse(BaseModel):
    """Тело ошибки FastAPI — используется в негативных тестах."""

    detail: str | list[dict]
