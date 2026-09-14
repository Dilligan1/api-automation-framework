"""
Smoke-тесты сервиса постов: лента, создание, чтение, удаление.
"""

import allure
import pytest

from config.base_test import BaseTest
from services.posts.api import PostAPI
from services.posts.payloads import CreatePostPayload


@allure.epic("Smoke")
@allure.feature("Посты")
class TestPostsSmoke(BaseTest):

    @pytest.mark.smoke
    @pytest.mark.critical
    @allure.story("Лента")
    @allure.title("GET /api/posts — список постов отдаётся с корректной пагинацией")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_list_posts(self, post_api: PostAPI) -> None:
        """
        Шаги:
        1. Запросить первую страницу постов (per_page=5)

        Ожидаемый результат:
        - HTTP 200 OK
        - page == 1, per_page == 5
        - items не больше per_page
        """
        with allure.step("GET /api/posts?page=1&per_page=5"):
            result = post_api.list_posts(page=1, per_page=5)

        with allure.step("Проверить конверт пагинации"):
            assert result.page == 1, f"Ожидалась страница 1, получена {result.page}"
            assert result.per_page == 5, f"Ожидался per_page=5, получен {result.per_page}"
            assert len(result.items) <= 5, (
                f"Вернулось больше элементов, чем per_page: {len(result.items)}"
            )

    @pytest.mark.smoke
    @pytest.mark.critical
    @allure.story("Создание поста")
    @allure.title("POST /api/posts — пост создаётся и доступен по id")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_and_read_post(self, post_api: PostAPI) -> None:
        """
        Шаги:
        1. Создать пост со сгенерированным текстом
        2. Прочитать его по id
        3. Удалить (тест не оставляет мусор на общем стенде)

        Ожидаемый результат:
        - HTTP 201 при создании, текст совпадает с отправленным
        - HTTP 200 при чтении, id совпадает
        """
        payload = CreatePostPayload(**self.gen.post())

        with allure.step("POST /api/posts"):
            created = post_api.create(payload)

        try:
            with allure.step("Проверить созданный пост"):
                assert created.content == payload.content, (
                    "Текст созданного поста не совпадает с отправленным"
                )
                assert created.likes_count == 0, "У нового поста не должно быть лайков"
                assert created.is_deleted is False, "Новый пост помечен удалённым"

            with allure.step(f"GET /api/posts/{created.id}"):
                fetched = post_api.get(str(created.id))
                assert fetched.id == created.id, "Прочитан не тот пост"
        finally:
            with allure.step("Удалить созданный пост"):
                post_api.delete(str(created.id))

    @pytest.mark.smoke
    @allure.story("Лента подписок")
    @allure.title("GET /api/posts/feed — персональная лента отдаётся")
    @allure.severity(allure.severity_level.NORMAL)
    def test_feed_available(self, post_api: PostAPI) -> None:
        """
        Шаги:
        1. Запросить персональную ленту подписок

        Ожидаемый результат:
        - HTTP 200 OK
        - конверт пагинации корректен (лента может быть пустой — это валидно)
        """
        with allure.step("GET /api/posts/feed"):
            result = post_api.get_feed()

        with allure.step("Проверить конверт ответа"):
            assert result.total >= 0, "Некорректное значение total"
            assert isinstance(result.items, list), "items не является списком"
