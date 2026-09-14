"""
Smoke-тесты сервиса авторизации.

Покрывают полный цикл токена: регистрация → логин → me → refresh → logout.
Регистрация создаёт нового пользователя на каждый прогон (DataGenerator),
поэтому тест повторно запускаем на том же стенде без сброса.
"""

import allure
import pytest

from auth.token_provider import TokenProvider, User
from config.base_test import BaseTest
from services.auth.api import AuthAPI
from services.auth.payloads import LoginPayload, RefreshPayload, RegisterPayload


@allure.epic("Smoke")
@allure.feature("Авторизация")
class TestAuthSmoke(BaseTest):

    @pytest.mark.smoke
    @pytest.mark.critical
    @allure.story("Регистрация")
    @allure.title("POST /api/auth/register — новый пользователь создаётся")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_new_user(self, auth_api: AuthAPI, registered_users: list) -> None:
        """
        Шаги:
        1. Сгенерировать данные нового пользователя
        2. Зарегистрировать его
        3. Отдать созданный аккаунт на уборку (деактивация правами админа)

        Ожидаемый результат:
        - HTTP 201 Created
        - email/username в ответе совпадают с отправленными
        - роль по умолчанию — user, аккаунт активен
        """
        data = self.gen.user()

        with allure.step(f"POST /api/auth/register — {data['username']}"):
            user = auth_api.register(RegisterPayload(**data))
            registered_users.append(str(user.id))

        with allure.step("Проверить созданного пользователя"):
            assert user.email == data["email"], "Email в ответе не совпадает с отправленным"
            assert user.username == data["username"], "Username в ответе не совпадает"
            assert user.role == "user", f"Ожидалась роль 'user', получена '{user.role}'"
            assert user.is_active is True, "Новый пользователь должен быть активен"

    @pytest.mark.smoke
    @pytest.mark.critical
    @allure.story("Логин")
    @allure.title("POST /api/auth/login — выдаётся пара токенов")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_returns_token_pair(
        self, auth_api: AuthAPI, token_provider: TokenProvider
    ) -> None:
        """
        Используется пользователь LONGREAD: под ним не логинится ни одна
        фикстура, поэтому явный вход в тесте не сталкивается с логином
        TokenProvider в ту же секунду (см. BUG-001 в docs/known-issues.md).

        Шаги:
        1. Взять учётные данные seed-пользователя LONGREAD
        2. Залогиниться

        Ожидаемый результат:
        - HTTP 200 OK
        - непустые access_token и refresh_token
        - token_type == "bearer"
        """
        email, password = token_provider.credentials(User.LONGREAD)

        with allure.step(f"POST /api/auth/login — {email}"):
            tokens = auth_api.login(LoginPayload(email=email, password=password))

        with allure.step("Проверить выданные токены"):
            assert tokens.access_token, "access_token пустой"
            assert tokens.refresh_token, "refresh_token пустой"
            assert tokens.token_type == "bearer", (
                f"Ожидался token_type='bearer', получен '{tokens.token_type}'"
            )

    @pytest.mark.smoke
    @allure.story("Текущий пользователь")
    @allure.title("GET /api/auth/me — профиль соответствует владельцу токена")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_me_matches_token_owner(
        self, http_client, token_active: str, token_provider: TokenProvider
    ) -> None:
        """
        Шаги:
        1. Запросить профиль по access-токену пользователя ACTIVE

        Ожидаемый результат:
        - HTTP 200 OK
        - email профиля совпадает с email из учётных данных
        """
        email, _ = token_provider.credentials(User.ACTIVE)
        api = AuthAPI(http_client, token_active)

        with allure.step("GET /api/auth/me"):
            me = api.get_me()

        with allure.step("Проверить владельца токена"):
            assert me.email == email, (
                f"Токен принадлежит другому пользователю: {me.email} вместо {email}"
            )

    @pytest.mark.smoke
    @pytest.mark.flaky
    @pytest.mark.xfail(
        reason="BUG-001: refresh в ту же секунду, что и логин, отдаёт 500 "
               "(UniqueViolation на refresh_tokens.token_hash). "
               "См. docs/known-issues.md",
        strict=False,
    )
    @allure.story("Обновление токена")
    @allure.title("POST /api/auth/refresh — по refresh-токену выдаётся новая пара")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.issue("docs/known-issues.md#bug-001", "BUG-001")
    def test_refresh_issues_new_pair(
        self, auth_api: AuthAPI, token_provider: TokenProvider
    ) -> None:
        """
        Шаги:
        1. Взять refresh-токен пользователя MEDIA (не ACTIVE — чтобы не инвалидировать
           токен, которым пользуются остальные тесты прогона)
        2. Обменять его на новую пару

        Ожидаемый результат:
        - HTTP 200 OK
        - выдан непустой access_token

        Известный дефект BUG-001: если между логином и refresh прошло меньше
        секунды, сервис генерирует идентичный токен и падает с 500.
        Тест помечен xfail нестрого — при разнесении вызовов во времени проходит.
        """
        refresh = token_provider.refresh_token_for(User.MEDIA)

        with allure.step("POST /api/auth/refresh"):
            tokens = auth_api.refresh(RefreshPayload(refresh_token=refresh))

        with allure.step("Проверить новую пару токенов"):
            assert tokens.access_token, "После refresh не выдан access_token"
            assert tokens.refresh_token, "После refresh не выдан refresh_token"
