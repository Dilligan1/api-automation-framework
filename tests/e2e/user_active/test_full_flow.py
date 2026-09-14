"""
E2E: сквозной флоу активного пользователя.

Автор — ACTIVE (верифицированный публичный аккаунт), читатель — MEDIA.
Вся логика сценария в tests/e2e/base_flow.py; здесь только привязка
к конкретному пользователю и Allure-разметка.
"""

import allure

from tests.e2e.base_flow import BaseFlow


@allure.epic("E2E")
@allure.feature("Активный пользователь")
@allure.story("Пост → реакция → комментарий → уведомление → удаление")
@allure.title("E2E: полный цикл поста активного пользователя")
class TestActiveUserFullFlow(BaseFlow):
    pass
