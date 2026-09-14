# Сервисный класс авторизации.
# Единственный сервис, который умеет работать без токена: регистрация и логин
# вызываются до его получения. Остальные методы используют _auth_headers.

import allure

from services.auth.endpoints import AuthEndpoints
from services.auth.models.responses import TokenResponse, UserResponse
from services.auth.payloads import LoginPayload, RefreshPayload, RegisterPayload
from utils.api_helper import APIHelper
from utils.http_client import HTTPClient


class AuthAPI(APIHelper):
    def __init__(self, client: HTTPClient, token: str | None = None) -> None:
        self.client = client
        self.token = token
        self.endpoints = AuthEndpoints()

    @allure.step("Регистрация нового пользователя")
    def register(
        self, payload: RegisterPayload, status_code: int = 201, success: bool = True
    ) -> UserResponse | None:
        response = self.client.post(
            self.endpoints.register, json=payload.model_dump(exclude_none=True)
        )
        return self._validate_response(response, UserResponse, status_code, success)

    @allure.step("Логин пользователя")
    def login(
        self, payload: LoginPayload, status_code: int = 200, success: bool = True
    ) -> TokenResponse | None:
        response = self.client.post(self.endpoints.login, json=payload.model_dump())
        return self._validate_response(response, TokenResponse, status_code, success)

    @allure.step("Обновление пары токенов по refresh-токену")
    def refresh(
        self, payload: RefreshPayload, status_code: int = 200, success: bool = True
    ) -> TokenResponse | None:
        response = self.client.post(self.endpoints.refresh, json=payload.model_dump())
        return self._validate_response(response, TokenResponse, status_code, success)

    @allure.step("Отзыв refresh-токена (logout)")
    def logout(
        self, payload: RefreshPayload, status_code: int = 204, success: bool = True
    ) -> None:
        response = self.client.post(
            self.endpoints.logout,
            json=payload.model_dump(),
            headers=self._auth_headers,
        )
        return self._validate_response(response, None, status_code, success)

    @allure.step("Профиль текущего пользователя")
    def get_me(self, status_code: int = 200, success: bool = True) -> UserResponse | None:
        response = self.client.get(self.endpoints.me, headers=self._auth_headers)
        return self._validate_response(response, UserResponse, status_code, success)
