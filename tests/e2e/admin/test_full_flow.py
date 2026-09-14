"""
E2E: сквозной флоу администратора.

Проверяет, что роль admin не ломает обычный пользовательский путь:
админ остаётся полноценным автором контента.
"""

import allure

from tests.e2e.base_flow import BaseFlow


@allure.epic("E2E")
@allure.feature("Администратор")
@allure.story("Пост → реакция → комментарий → уведомление → удаление")
@allure.title("E2E: полный цикл поста администратора")
class TestAdminFullFlow(BaseFlow):
    pass
