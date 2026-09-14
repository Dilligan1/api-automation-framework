# Модели запросов сервиса пользователей.

from pydantic import BaseModel


class UpdateMePayload(BaseModel):
    """PATCH /users/me. Все поля опциональны — отправляем только изменяемые."""

    display_name: str | None = None
    bio: str | None = None      # до 500 символов
    is_private: bool | None = None
