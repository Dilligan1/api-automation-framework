"""
Негативные сценарии разграничения прав.

Ключевая проверка безопасности проекта: админские методы недоступны
обычному пользователю и анонимному клиенту.
"""

import allure
import pytest

from config.base_test import BaseTest
from services.admin.api import AdminAPI


@allure.epic("Negative")
@allure.feature("Администрирование")
class TestAdminAccessNegative(BaseTest):

    @pytest.mark.negative
    @pytest.mark.critical
    @allure.story("Разграничение прав")
    @allure.title("GET /api/admin/stats — обычному пользователю запрещено (403)")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_stats_forbidden_for_user(self, admin_api_as_user: AdminAPI) -> None:
        """
        Шаги:
        1. Запросить админскую статистику токеном обычного пользователя

        Ожидаемый результат: HTTP 403 Forbidden
        """
        with allure.step("GET /api/admin/stats от роли user"):
            admin_api_as_user.get_stats(status_code=403, success=False)

    @pytest.mark.negative
    @pytest.mark.critical
    @allure.story("Разграничение прав")
    @allure.title("GET /api/admin/users — обычному пользователю запрещено (403)")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_user_list_forbidden_for_user(self, admin_api_as_user: AdminAPI) -> None:
        """Ожидаемый результат: HTTP 403 Forbidden."""
        with allure.step("GET /api/admin/users от роли user"):
            admin_api_as_user.list_users(status_code=403, success=False)

    @pytest.mark.negative
    @allure.story("Разграничение прав")
    @allure.title("GET /api/admin/stats — без токена запрещено (403)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_stats_requires_auth(self, http_client) -> None:
        """
        Анонимный клиент не должен попадать в админку.

        Бэкенд на FastAPI отдаёт здесь 403 "Not authenticated", а не 401:
        схема HTTPBearer по умолчанию возвращает 403 при отсутствующем
        заголовке Authorization. Ожидание зафиксировано по фактическому
        поведению сервиса.
        """
        anonymous = AdminAPI(http_client, token="")

        with allure.step("GET /api/admin/stats без Authorization"):
            anonymous.get_stats(status_code=403, success=False)
