# Pydantic-модели ответов сервиса авторизации.

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TokenResponse(BaseModel):
    """POST /auth/login и POST /auth/refresh."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """POST /auth/register, GET /auth/me, а также профиль в сервисе users."""

    id: UUID
    email: str
    username: str
    display_name: str
    bio: str | None = None
    avatar_url: str | None = None
    cover_url: str | None = None
    role: str
    is_active: bool
    is_verified: bool
    is_private: bool
    created_at: datetime
    updated_at: datetime
    followers_count: int = 0
    following_count: int = 0
    posts_count: int = 0
    is_following: bool = False
    is_followed_by: bool = False
