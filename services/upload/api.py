# Сервисный класс загрузки изображений.
# Лимит 5 MB и белый список типов (jpeg/png/gif/webp) — границы в config/test_data.py.

import allure

from config.headers import MULTIPART_OVERRIDE
from services.upload.endpoints import UploadEndpoints
from services.upload.models.responses import UploadImageResponse
from utils.api_helper import APIHelper
from utils.http_client import HTTPClient


class UploadAPI(APIHelper):
    def __init__(self, client: HTTPClient, token: str) -> None:
        self.client = client
        self.token = token
        self.endpoints = UploadEndpoints()

    @allure.step("Загрузка изображения {filename} ({content_type})")
    def image(
        self,
        content: bytes,
        filename: str = "picture.png",
        content_type: str = "image/png",
        **kwargs,
    ) -> UploadImageResponse:
        # Content-Type сбрасывается — requests сам проставит boundary
        headers = {**self._auth_headers, **MULTIPART_OVERRIDE}
        response = self.client.post(
            self.endpoints.image,
            files={"file": (filename, content, content_type)},
            headers=headers,
        )
        return self._validate_response(response, UploadImageResponse, **kwargs)
