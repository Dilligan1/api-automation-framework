# Сервисный класс постов: лента, полный CRUD, репост, закрепление.
#
# Жизненный цикл поста (см. docs/status_machine.md):
#   created -> edited (окно 15 мин) -> soft-deleted (is_deleted=true)
#   pinned/unpinned — независимый флаг, не более одного закреплённого поста.

import allure

from services.common.models.responses import PaginatedResponse, PostResponse
from services.posts.endpoints import PostEndpoints
from services.posts.payloads import CreatePostPayload, RepostPayload, UpdatePostPayload
from utils.api_helper import APIHelper
from utils.http_client import HTTPClient


class PostAPI(APIHelper):
    def __init__(self, client: HTTPClient, token: str) -> None:
        self.client = client
        self.token = token
        self.endpoints = PostEndpoints()

    @allure.step("Список всех постов (page={page})")
    def list_posts(
        self, page: int = 1, per_page: int = 20, hashtag: str | None = None, **kwargs
    ) -> PaginatedResponse[PostResponse]:
        params = {"page": page, "per_page": per_page}
        if hashtag is not None:
            params["hashtag"] = hashtag
        response = self.client.get(
            self.endpoints.posts, params=params, headers=self._auth_headers
        )
        return self._validate_response(response, PaginatedResponse[PostResponse], **kwargs)

    @allure.step("Персональная лента подписок")
    def get_feed(
        self, page: int = 1, per_page: int = 20, **kwargs
    ) -> PaginatedResponse[PostResponse]:
        response = self.client.get(
            self.endpoints.feed,
            params={"page": page, "per_page": per_page},
            headers=self._auth_headers,
        )
        return self._validate_response(response, PaginatedResponse[PostResponse], **kwargs)

    @allure.step("Создание поста")
    def create(
        self, payload: CreatePostPayload, status_code: int = 201, **kwargs
    ) -> PostResponse:
        response = self.client.post(
            self.endpoints.posts,
            json=payload.model_dump(exclude_none=True),
            headers=self._auth_headers,
        )
        return self._validate_response(response, PostResponse, status_code, **kwargs)

    @allure.step("Получение поста {post_id}")
    def get(self, post_id: str, **kwargs) -> PostResponse:
        response = self.client.get(
            self.endpoints.by_id(post_id), headers=self._auth_headers
        )
        return self._validate_response(response, PostResponse, **kwargs)

    @allure.step("Редактирование поста {post_id}")
    def update(self, post_id: str, payload: UpdatePostPayload, **kwargs) -> PostResponse:
        response = self.client.patch(
            self.endpoints.by_id(post_id),
            json=payload.model_dump(),
            headers=self._auth_headers,
        )
        return self._validate_response(response, PostResponse, **kwargs)

    @allure.step("Удаление поста {post_id}")
    def delete(self, post_id: str, status_code: int = 204, **kwargs) -> None:
        response = self.client.delete(
            self.endpoints.by_id(post_id), headers=self._auth_headers
        )
        return self._validate_response(response, None, status_code, **kwargs)

    @allure.step("Репост поста {post_id}")
    def repost(
        self, post_id: str, payload: RepostPayload | None = None, status_code: int = 201, **kwargs
    ) -> PostResponse:
        payload = payload or RepostPayload()
        response = self.client.post(
            self.endpoints.repost(post_id),
            json=payload.model_dump(exclude_none=True),
            headers=self._auth_headers,
        )
        return self._validate_response(response, PostResponse, status_code, **kwargs)

    @allure.step("Закрепление поста {post_id}")
    def pin(self, post_id: str, status_code: int = 204, **kwargs) -> None:
        response = self.client.post(
            self.endpoints.pin(post_id), headers=self._auth_headers
        )
        return self._validate_response(response, None, status_code, **kwargs)

    @allure.step("Открепление поста {post_id}")
    def unpin(self, post_id: str, status_code: int = 204, **kwargs) -> None:
        response = self.client.delete(
            self.endpoints.pin(post_id), headers=self._auth_headers
        )
        return self._validate_response(response, None, status_code, **kwargs)
