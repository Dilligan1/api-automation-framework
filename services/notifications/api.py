# Сервисный класс уведомлений.
# Уведомления создаются побочным эффектом действий других пользователей —
# поэтому проверяются в E2E-флоу, а не изолированно.

import allure

from services.common.models.responses import PaginatedResponse
from services.notifications.endpoints import NotificationEndpoints
from services.notifications.models.responses import (
    NotificationResponse,
    UnreadCountResponse,
)
from utils.api_helper import APIHelper
from utils.http_client import HTTPClient


class NotificationAPI(APIHelper):
    def __init__(self, client: HTTPClient, token: str) -> None:
        self.client = client
        self.token = token
        self.endpoints = NotificationEndpoints()

    @allure.step("Список уведомлений")
    def list_notifications(
        self, unread_only: bool | None = None, **kwargs
    ) -> PaginatedResponse[NotificationResponse]:
        params = {} if unread_only is None else {"unread_only": unread_only}
        response = self.client.get(
            self.endpoints.notifications, params=params, headers=self._auth_headers
        )
        return self._validate_response(
            response, PaginatedResponse[NotificationResponse], **kwargs
        )

    @allure.step("Счётчик непрочитанных уведомлений")
    def get_unread_count(self, **kwargs) -> UnreadCountResponse:
        response = self.client.get(self.endpoints.unread_count, headers=self._auth_headers)
        return self._validate_response(response, UnreadCountResponse, **kwargs)

    @allure.step("Отметить уведомление {notification_id} прочитанным")
    def mark_read(self, notification_id: str, status_code: int = 204, **kwargs) -> None:
        response = self.client.post(
            self.endpoints.read(notification_id), headers=self._auth_headers
        )
        return self._validate_response(response, None, status_code, **kwargs)

    @allure.step("Отметить все уведомления прочитанными")
    def mark_all_read(self, status_code: int = 204, **kwargs) -> None:
        response = self.client.post(self.endpoints.read_all, headers=self._auth_headers)
        return self._validate_response(response, None, status_code, **kwargs)
