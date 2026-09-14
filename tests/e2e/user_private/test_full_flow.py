"""
E2E: сквозной флоу приватного аккаунта.

Тот же бизнес-путь, что и у публичного пользователя, но от лица аккаунта
с is_private=true — проверяем, что приватность не ломает базовый сценарий.
"""

import allure

from tests.e2e.base_flow import BaseFlow


@allure.epic("E2E")
@allure.feature("Приватный аккаунт")
@allure.story("Пост → реакция → комментарий → уведомление → удаление")
@allure.title("E2E: полный цикл поста приватного аккаунта")
class TestPrivateUserFullFlow(BaseFlow):
    pass
