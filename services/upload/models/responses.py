# Модели ответов сервиса загрузки файлов.

from pydantic import BaseModel


class UploadImageResponse(BaseModel):
    """POST /upload/image — путь, который затем кладётся в image_url поста."""

    url: str
    filename: str | None = None
    size: int | None = None
    content_type: str | None = None
