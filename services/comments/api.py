# Сервисный класс комментариев: плоский список под постом, ответы (до 3 уровней),
# редактирование и удаление.

import allure

from services.comments.endpoints import CommentEndpoints
from services.comments.models.responses import CommentResponse
from services.comments.payloads import CreateCommentPayload, UpdateCommentPayload
from services.common.models.responses import PaginatedResponse
from utils.api_helper import APIHelper
from utils.http_client import HTTPClient


class CommentAPI(APIHelper):
    def __init__(self, client: HTTPClient, token: str) -> None:
        self.client = client
        self.token = token
        self.endpoints = CommentEndpoints()

    @allure.step("Комментарии поста {post_id}")
    def list_comments(
        self, post_id: str, page: int = 1, per_page: int = 20, **kwargs
    ) -> PaginatedResponse[CommentResponse]:
        response = self.client.get(
            self.endpoints.of_post(post_id),
            params={"page": page, "per_page": per_page},
            headers=self._auth_headers,
        )
        return self._validate_response(response, PaginatedResponse[CommentResponse], **kwargs)

    @allure.step("Комментирование поста {post_id}")
    def create(
        self, post_id: str, payload: CreateCommentPayload, status_code: int = 201, **kwargs
    ) -> CommentResponse:
        response = self.client.post(
            self.endpoints.of_post(post_id),
            json=payload.model_dump(),
            headers=self._auth_headers,
        )
        return self._validate_response(response, CommentResponse, status_code, **kwargs)

    @allure.step("Редактирование комментария {comment_id}")
    def update(
        self, comment_id: str, payload: UpdateCommentPayload, **kwargs
    ) -> CommentResponse:
        response = self.client.patch(
            self.endpoints.by_id(comment_id),
            json=payload.model_dump(),
            headers=self._auth_headers,
        )
        return self._validate_response(response, CommentResponse, **kwargs)

    @allure.step("Удаление комментария {comment_id}")
    def delete(self, comment_id: str, status_code: int = 204, **kwargs) -> None:
        response = self.client.delete(
            self.endpoints.by_id(comment_id), headers=self._auth_headers
        )
        return self._validate_response(response, None, status_code, **kwargs)

    @allure.step("Ответы на комментарий {comment_id}")
    def list_replies(
        self, comment_id: str, **kwargs
    ) -> PaginatedResponse[CommentResponse]:
        response = self.client.get(
            self.endpoints.replies(comment_id), headers=self._auth_headers
        )
        return self._validate_response(response, PaginatedResponse[CommentResponse], **kwargs)

    @allure.step("Ответ на комментарий {comment_id}")
    def reply(
        self, comment_id: str, payload: CreateCommentPayload, status_code: int = 201, **kwargs
    ) -> CommentResponse:
        response = self.client.post(
            self.endpoints.replies(comment_id),
            json=payload.model_dump(),
            headers=self._auth_headers,
        )
        return self._validate_response(response, CommentResponse, status_code, **kwargs)
