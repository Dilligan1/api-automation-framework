# Сервисный класс администрирования: статистика, управление пользователями,
# модерация контента.
#
# Доступ только ролям admin/moderator — те же методы от обычного пользователя
# должны отдавать 403 (см. tests/negative/test_admin_negative.py).

import allure

from services.admin.endpoints import AdminEndpoints
from services.admin.models.responses import AdminStatsResponse
from services.admin.payloads import AdminUserUpdatePayload
from services.auth.models.responses import UserResponse
from services.common.models.responses import PaginatedResponse, PostResponse
from utils.api_helper import APIHelper
from utils.http_client import HTTPClient


class AdminAPI(APIHelper):
    def __init__(self, client: HTTPClient, token: str) -> None:
        self.client = client
        self.token = token
        self.endpoints = AdminEndpoints()

    @allure.step("Статистика дашборда")
    def get_stats(self, **kwargs) -> AdminStatsResponse:
        response = self.client.get(self.endpoints.stats, headers=self._auth_headers)
        return self._validate_response(response, AdminStatsResponse, **kwargs)

    @allure.step("Список всех пользователей (admin)")
    def list_users(
        self, page: int = 1, per_page: int = 20, search: str | None = None, **kwargs
    ) -> PaginatedResponse[UserResponse]:
        params = {"page": page, "per_page": per_page}
        if search is not None:
            params["search"] = search
        response = self.client.get(
            self.endpoints.users, params=params, headers=self._auth_headers
        )
        return self._validate_response(response, PaginatedResponse[UserResponse], **kwargs)

    @allure.step("Изменение пользователя {user_id} (роль/бан/верификация)")
    def update_user(
        self, user_id: str, payload: AdminUserUpdatePayload, **kwargs
    ) -> UserResponse:
        response = self.client.patch(
            self.endpoints.user(user_id),
            json=payload.model_dump(exclude_none=True),
            headers=self._auth_headers,
        )
        return self._validate_response(response, UserResponse, **kwargs)

    @allure.step("Деактивация пользователя {user_id}")
    def deactivate_user(self, user_id: str, status_code: int = 204, **kwargs) -> None:
        response = self.client.delete(
            self.endpoints.user(user_id), headers=self._auth_headers
        )
        return self._validate_response(response, None, status_code, **kwargs)

    @allure.step("Список всех постов (admin)")
    def list_posts(
        self, page: int = 1, per_page: int = 20, **kwargs
    ) -> PaginatedResponse[PostResponse]:
        response = self.client.get(
            self.endpoints.posts,
            params={"page": page, "per_page": per_page},
            headers=self._auth_headers,
        )
        return self._validate_response(response, PaginatedResponse[PostResponse], **kwargs)

    @allure.step("Модераторское удаление поста {post_id}")
    def delete_post(self, post_id: str, status_code: int = 204, **kwargs) -> None:
        response = self.client.delete(
            self.endpoints.post(post_id), headers=self._auth_headers
        )
        return self._validate_response(response, None, status_code, **kwargs)
