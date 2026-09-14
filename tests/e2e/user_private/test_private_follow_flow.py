"""
E2E: жизненный цикл подписки на приватный аккаунт.

Ключевой статусный переход проекта: pending → accepted.
Единственный тест, который его покрывает целиком.
"""

import allure
import pytest

from config.base_test import BaseTest
from config.test_data import USERNAME_ACTIVE, USERNAME_PRIVATE
from services.follows.api import FollowAPI


@allure.epic("E2E")
@allure.feature("Приватный аккаунт")
@allure.story("Запрос на подписку: pending → accepted")
class TestPrivateFollowFlow(BaseTest):

    @pytest.mark.e2e
    @pytest.mark.critical
    @allure.title("E2E: подписка на приватный аккаунт подтверждается владельцем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_follow_request_lifecycle(
        self, follow_api: FollowAPI, follow_api_private: FollowAPI
    ) -> None:
        """
        Шаги:
        1. ACTIVE подписывается на приватный аккаунт PRIVATE
        2. Подписка создаётся в статусе pending
        3. Владелец приватного аккаунта видит входящий запрос
        4. Владелец подтверждает запрос — статус становится accepted
        5. ACTIVE отписывается, состояние стенда восстанавливается

        Ожидаемый результат: статусы меняются строго pending → accepted,
        запрос виден владельцу до подтверждения.
        """
        with allure.step("Предусловие: снять подписку, если она осталась от прошлого прогона"):
            # 404 здесь — штатная ситуация: подписки не было
            try:
                follow_api.unfollow(USERNAME_PRIVATE)
            except AssertionError:
                pass

        with allure.step(f"1. Подписка на приватный аккаунт @{USERNAME_PRIVATE}"):
            follow = follow_api.follow(USERNAME_PRIVATE)

        try:
            with allure.step("2. Проверить, что подписка ушла в pending"):
                assert follow.status == "pending", (
                    f"Подписка на приватный аккаунт должна быть 'pending', "
                    f"получено '{follow.status}'"
                )

            with allure.step("3. Владелец видит входящий запрос"):
                requests = follow_api_private.get_requests()
                pending_from_active = [
                    r for r in requests.items if r.follower.username == USERNAME_ACTIVE
                ]
                assert pending_from_active, (
                    f"Запрос от @{USERNAME_ACTIVE} не найден в списке входящих"
                )

            with allure.step("4. Владелец подтверждает запрос"):
                accepted = follow_api_private.accept(str(follow.id))
                assert accepted.status == "accepted", (
                    f"После подтверждения ожидался статус 'accepted', "
                    f"получено '{accepted.status}'"
                )
        finally:
            with allure.step("5. Отписка — состояние стенда восстановлено"):
                follow_api.unfollow(USERNAME_PRIVATE)
