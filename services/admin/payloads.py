# Модели запросов сервиса администрирования.

from pydantic import BaseModel


class AdminUserUpdatePayload(BaseModel):
    """
    PATCH /admin/users/{id}.

    role        — user | moderator | admin
    is_active   — false = бан пользователя
    is_verified — галочка верификации
    """

    role: str | None = None
    is_active: bool | None = None
    is_verified: bool | None = None
