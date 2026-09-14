# Модели ответов системных эндпоинтов.

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    database: str | None = None


class ResetResponse(BaseModel):
    """POST /reset — пересоздаёт схему и заново заливает seed-данные (~2 сек)."""

    status: str | None = None
    message: str | None = None
