# Сервисный класс закладок.

import allure

from services.bookmarks.endpoints import BookmarkEndpoints
from services.common.models.responses import PaginatedResponse, PostResponse
from utils.api_helper import APIHelper
from utils.http_client import HTTPClient


class BookmarkAPI(APIHelper):
    def __init__(self, client: HTTPClient, token: str) -> None:
        self.client = client
        self.token = token
        self.endpoints = BookmarkEndpoints()

    @allure.step("Список закладок")
    def list_bookmarks(
        self, page: int = 1, per_page: int = 20, **kwargs
    ) -> PaginatedResponse[PostResponse]:
        response = self.client.get(
            self.endpoints.bookmarks,
            params={"page": page, "per_page": per_page},
            headers=self._auth_headers,
        )
        return self._validate_response(response, PaginatedResponse[PostResponse], **kwargs)

    @allure.step("Добавление поста {post_id} в закладки")
    def add(self, post_id: str, status_code: int = 201, **kwargs) -> None:
        response = self.client.post(
            self.endpoints.of_post(post_id), headers=self._auth_headers
        )
        return self._validate_response(response, None, status_code, **kwargs)

    @allure.step("Удаление поста {post_id} из закладок")
    def remove(self, post_id: str, status_code: int = 204, **kwargs) -> None:
        response = self.client.delete(
            self.endpoints.of_post(post_id), headers=self._auth_headers
        )
        return self._validate_response(response, None, status_code, **kwargs)
