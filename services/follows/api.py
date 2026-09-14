# Сервисный класс подписок.
# Ключевой статусный переход проекта: подписка на приватный аккаунт создаётся
# в статусе pending и становится accepted только после accept владельцем.

import allure

from services.common.models.responses import PaginatedResponse
from services.follows.endpoints import FollowEndpoints
from services.follows.models.responses import FollowRequestResponse, FollowResponse
from utils.api_helper import APIHelper
from utils.http_client import HTTPClient


class FollowAPI(APIHelper):
    def __init__(self, client: HTTPClient, token: str) -> None:
        self.client = client
        self.token = token
        self.endpoints = FollowEndpoints()

    @allure.step("Подписка на @{username}")
    def follow(self, username: str, status_code: int = 201, **kwargs) -> FollowResponse:
        response = self.client.post(
            self.endpoints.follow(username), headers=self._auth_headers
        )
        return self._validate_response(response, FollowResponse, status_code, **kwargs)

    @allure.step("Отписка от @{username}")
    def unfollow(self, username: str, status_code: int = 204, **kwargs) -> None:
        response = self.client.delete(
            self.endpoints.follow(username), headers=self._auth_headers
        )
        return self._validate_response(response, None, status_code, **kwargs)

    @allure.step("Входящие запросы на подписку")
    def get_requests(self, **kwargs) -> PaginatedResponse[FollowRequestResponse]:
        response = self.client.get(self.endpoints.requests, headers=self._auth_headers)
        return self._validate_response(
            response, PaginatedResponse[FollowRequestResponse], **kwargs
        )

    @allure.step("Подтверждение запроса на подписку {follow_id}")
    def accept(self, follow_id: str, **kwargs) -> FollowResponse:
        response = self.client.post(
            self.endpoints.accept(follow_id), headers=self._auth_headers
        )
        return self._validate_response(response, FollowResponse, **kwargs)

    @allure.step("Отклонение запроса на подписку {follow_id}")
    def reject(self, follow_id: str, status_code: int = 204, **kwargs) -> None:
        response = self.client.post(
            self.endpoints.reject(follow_id), headers=self._auth_headers
        )
        return self._validate_response(response, None, status_code, **kwargs)
