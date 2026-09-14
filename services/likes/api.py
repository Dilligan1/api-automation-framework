# Сервисный класс реакций на посты и комментарии.
# Повторный лайк тем же пользователем меняет тип реакции, а не создаёт вторую.

import allure

from services.common.models.responses import PaginatedResponse
from services.likes.endpoints import LikeEndpoints
from services.likes.models.responses import LikeResponse
from services.likes.payloads import ReactionPayload
from utils.api_helper import APIHelper
from utils.http_client import HTTPClient


class LikeAPI(APIHelper):
    def __init__(self, client: HTTPClient, token: str) -> None:
        self.client = client
        self.token = token
        self.endpoints = LikeEndpoints()

    @allure.step("Реакция на пост {post_id}")
    def like_post(
        self, post_id: str, payload: ReactionPayload | None = None, status_code: int = 201, **kwargs
    ) -> LikeResponse:
        payload = payload or ReactionPayload()
        response = self.client.post(
            self.endpoints.post_like(post_id),
            json=payload.model_dump(),
            headers=self._auth_headers,
        )
        return self._validate_response(response, LikeResponse, status_code, **kwargs)

    @allure.step("Снятие реакции с поста {post_id}")
    def unlike_post(self, post_id: str, status_code: int = 204, **kwargs) -> None:
        response = self.client.delete(
            self.endpoints.post_like(post_id), headers=self._auth_headers
        )
        return self._validate_response(response, None, status_code, **kwargs)

    @allure.step("Список реакций поста {post_id}")
    def get_post_likes(self, post_id: str, **kwargs) -> PaginatedResponse[LikeResponse]:
        response = self.client.get(
            self.endpoints.post_likes(post_id), headers=self._auth_headers
        )
        return self._validate_response(response, PaginatedResponse[LikeResponse], **kwargs)

    @allure.step("Реакция на комментарий {comment_id}")
    def like_comment(
        self, comment_id: str, payload: ReactionPayload | None = None, status_code: int = 201, **kwargs
    ) -> LikeResponse:
        payload = payload or ReactionPayload()
        response = self.client.post(
            self.endpoints.comment_like(comment_id),
            json=payload.model_dump(),
            headers=self._auth_headers,
        )
        return self._validate_response(response, LikeResponse, status_code, **kwargs)

    @allure.step("Снятие реакции с комментария {comment_id}")
    def unlike_comment(self, comment_id: str, status_code: int = 204, **kwargs) -> None:
        response = self.client.delete(
            self.endpoints.comment_like(comment_id), headers=self._auth_headers
        )
        return self._validate_response(response, None, status_code, **kwargs)
