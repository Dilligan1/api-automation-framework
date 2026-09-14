"""
Негативные сценарии авторизации.

Проверяется, что сервис отвечает корректным кодом ошибки, а не 500
и не выдаёт токен там, где не должен.
"""

import allure
import pytest

from auth.token_provider import TokenProvider, User
from config.base_test import BaseTest
from services.auth.api import AuthAPI
from services.auth.payloads import LoginPayload, RefreshPayload, RegisterPayload


@allure.epic("Negative")
@allure.feature("Авторизация")
class TestAuthNegative(BaseTest):

    @pytest.mark.negative
    @allure.story("Логин")
    @allure.title("POST /api/auth/login — неверный пароль отклоняется (401)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_wrong_password(
        self, auth_api: AuthAPI, token_provider: TokenProvider
    ) -> None:
        """
        Шаги:
        1. Взять существующий email и заведомо неверный пароль
        2. Попытаться залогиниться

        Ожидаемый результат:
        - HTTP 401 Unauthorized, токен не выдан
        """
        email, _ = token_provider.credentials(User.ACTIVE)

        with allure.step("POST /api/auth/login с неверным паролем"):
            auth_api.login(
                LoginPayload(email=email, password="definitely-wrong-password"),
                status_code=401,
                success=False,
            )

    @pytest.mark.negative
    @allure.story("Логин")
    @allure.title("POST /api/auth/login — несуществующий email отклоняется (401)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_unknown_email(self, auth_api: AuthAPI) -> None:
        """
        Ожидаемый результат: HTTP 401 — тот же код, что и при неверном пароле
        (сервис не должен раскрывать, существует ли аккаунт).
        """
        with allure.step("POST /api/auth/login с несуществующим email"):
            auth_api.login(
                LoginPayload(email=self.gen.unique_email(), password="whatever123"),
                status_code=401,
                success=False,
            )

    @pytest.mark.negative
    @allure.story("Регистрация")
    @allure.title("POST /api/auth/register — занятый email отклоняется (409)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_duplicate_email(
        self, auth_api: AuthAPI, token_provider: TokenProvider
    ) -> None:
        """
        Шаги:
        1. Взять email существующего seed-пользователя
        2. Попытаться зарегистрировать на него нового пользователя

        Ожидаемый результат: HTTP 409 Conflict с error_code=CONFLICT
        """
        email, _ = token_provider.credentials(User.ACTIVE)
        data = self.gen.user(email=email)

        with allure.step("POST /api/auth/register с занятым email"):
            auth_api.register(RegisterPayload(**data), status_code=409, success=False)

    @pytest.mark.negative
    @allure.story("Регистрация")
    @allure.title("POST /api/auth/register — короткий пароль отклоняется (422)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_register_short_password(self, auth_api: AuthAPI) -> None:
        """
        Пароль короче 6 символов не проходит валидацию Pydantic на бэкенде.

        Ожидаемый результат: HTTP 422 Unprocessable Entity
        """
        data = self.gen.user(password="12345")

        with allure.step("POST /api/auth/register с паролем из 5 символов"):
            auth_api.register(RegisterPayload(**data), status_code=422, success=False)

    @pytest.mark.negative
    @allure.story("Обновление токена")
    @allure.title("POST /api/auth/refresh — мусорный refresh-токен отклоняется (401)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_refresh_invalid_token(self, auth_api: AuthAPI) -> None:
        """Ожидаемый результат: HTTP 401 Unauthorized."""
        with allure.step("POST /api/auth/refresh с невалидным токеном"):
            auth_api.refresh(
                RefreshPayload(refresh_token="not-a-real-token"),
                status_code=401,
                success=False,
            )
