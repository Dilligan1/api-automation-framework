# Pydantic-модели запросов сервиса авторизации.
# Имена полей совпадают с именами в API — намеренно.
# Применение: payload.model_dump(exclude_none=True).

from pydantic import BaseModel


class RegisterPayload(BaseModel):
    """POST /auth/register. username: ^[a-zA-Z0-9_]+$, 3–30; password: 6–128."""

    email: str
    username: str
    password: str
    display_name: str


class LoginPayload(BaseModel):
    """POST /auth/login."""

    email: str
    password: str


class RefreshPayload(BaseModel):
    """POST /auth/refresh и POST /auth/logout."""

    refresh_token: str
