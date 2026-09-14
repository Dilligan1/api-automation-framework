# Сервисный класс пользователей: каталог, профиль, редактирование, аватар,
# списки подписчиков и подписок.

import allure

from config.headers import MULTIPART_OVERRIDE
from services.auth.models.responses import UserResponse
from services.common.models.responses import PaginatedResponse, PostResponse, UserBrief
from services.users.endpoints import UserEndpoints
from services.users.payloads import UpdateMePayload
from utils.api_helper import APIHelper
from utils.http_client import HTTPClient


class UserAPI(APIHelper):
    def __init__(self, client: HTTPClient, token: str) -> None:
        self.client = client
        self.token = token
        self.endpoints = UserEndpoints()

    @allure.step("Список пользователей (page={page}, per_page={per_page})")
    def list_users(
        self, page: int = 1, per_page: int = 20, search: str | None = None, **kwargs
    ) -> PaginatedResponse[UserBrief]:
        params = {"page": page, "per_page": per_page}
        if search is not None:
            params["search"] = search
        response = self.client.get(
            self.endpoints.list_users, params=params, headers=self._auth_headers
        )
        return self._validate_response(response, PaginatedResponse[UserBrief], **kwargs)

    @allure.step("Рекомендации к подписке")
    def get_suggestions(self, **kwargs) -> list[UserBrief]:
        response = self.client.get(self.endpoints.suggestions, headers=self._auth_headers)
        return self._validate_response(response, UserBrief, **kwargs)

    @allure.step("Профиль пользователя @{username}")
    def get_user(self, username: str, **kwargs) -> UserResponse:
        response = self.client.get(
            self.endpoints.by_username(username), headers=self._auth_headers
        )
        return self._validate_response(response, UserResponse, **kwargs)

    @allure.step("Изменение своего профиля")
    def update_me(self, payload: UpdateMePayload, **kwargs) -> UserResponse:
        response = self.client.patch(
            self.endpoints.update_me,
            json=payload.model_dump(exclude_none=True),
            headers=self._auth_headers,
        )
        return self._validate_response(response, UserResponse, **kwargs)

    @allure.step("Загрузка аватара ({filename})")
    def upload_avatar(
        self, content: bytes, filename: str = "avatar.png", content_type: str = "image/png", **kwargs
    ) -> UserResponse:
        # Content-Type сбрасывается: requests сам проставит boundary для multipart
        headers = {**self._auth_headers, **MULTIPART_OVERRIDE}
        response = self.client.post(
            self.endpoints.avatar,
            files={"file": (filename, content, content_type)},
            headers=headers,
        )
        return self._validate_response(response, UserResponse, **kwargs)

    @allure.step("Удаление аватара")
    def delete_avatar(self, status_code: int = 204, **kwargs) -> None:
        response = self.client.delete(self.endpoints.avatar, headers=self._auth_headers)
        return self._validate_response(response, None, status_code, **kwargs)

    @allure.step("Посты пользователя @{username}")
    def get_user_posts(
        self, username: str, page: int = 1, per_page: int = 20, **kwargs
    ) -> PaginatedResponse[PostResponse]:
        response = self.client.get(
            self.endpoints.posts(username),
            params={"page": page, "per_page": per_page},
            headers=self._auth_headers,
        )
        return self._validate_response(response, PaginatedResponse[PostResponse], **kwargs)

    @allure.step("Подписчики @{username}")
    def get_followers(self, username: str, **kwargs) -> PaginatedResponse[UserBrief]:
        response = self.client.get(
            self.endpoints.followers(username), headers=self._auth_headers
        )
        return self._validate_response(response, PaginatedResponse[UserBrief], **kwargs)

    @allure.step("Подписки @{username}")
    def get_following(self, username: str, **kwargs) -> PaginatedResponse[UserBrief]:
        response = self.client.get(
            self.endpoints.following(username), headers=self._auth_headers
        )
        return self._validate_response(response, PaginatedResponse[UserBrief], **kwargs)
