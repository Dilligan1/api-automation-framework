"""
Smoke-тест системных эндпоинтов.

Цель: до всех остальных тестов убедиться, что стенд поднят и БД доступна.
Если этот тест красный — остальные результаты прогона смысла не имеют.
"""

import allure
import pytest

from config.base_test import BaseTest
from services.system.api import SystemAPI


@allure.epic("Smoke")
@allure.feature("Система")
class TestSystemSmoke(BaseTest):

    @pytest.mark.smoke
    @pytest.mark.critical
    @allure.story("Доступность стенда")
    @allure.title("GET /api/health — стенд и БД доступны")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_health_check(self, system_api: SystemAPI) -> None:
        """
        Шаги:
        1. Запросить health-check стенда

        Ожидаемый результат:
        - HTTP 200 OK
        - status == "healthy"
        - database == "connected"
        """
        with allure.step("GET /api/health"):
            result = system_api.health()

        with allure.step("Проверить статус стенда"):
            assert result.status == "healthy", (
                f"Стенд недоступен или деградировал: status='{result.status}'"
            )
            assert result.database == "connected", (
                f"Бэкенд не видит БД: database='{result.database}'"
            )
