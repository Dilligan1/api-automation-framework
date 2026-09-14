"""
Негативные сценарии и границы сервиса постов.
"""

import allure
import pytest

from config.base_test import BaseTest
from config.test_data import POST_CONTENT_MAX
from services.posts.api import PostAPI
from services.posts.payloads import CreatePostPayload, UpdatePostPayload


@allure.epic("Negative")
@allure.feature("Посты")
class TestPostsNegative(BaseTest):

    @pytest.mark.negative
    @allure.story("Границы контента")
    @allure.title(f"POST /api/posts — текст длиннее {POST_CONTENT_MAX} символов отклоняется (422)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_content_over_limit(self, post_api: PostAPI) -> None:
        """
        Шаги:
        1. Создать пост с текстом на 1 символ длиннее лимита

        Ожидаемый результат: HTTP 422 Unprocessable Entity
        """
        payload = CreatePostPayload(content=self.gen.text_of_length(POST_CONTENT_MAX + 1))

        with allure.step(f"POST /api/posts с текстом {POST_CONTENT_MAX + 1} символов"):
            post_api.create(payload, status_code=422, success=False)

    @pytest.mark.negative
    @allure.story("Границы контента")
    @allure.title("POST /api/posts — пустой текст отклоняется (422)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_content(self, post_api: PostAPI) -> None:
        """Ожидаемый результат: HTTP 422 — content имеет min_length=1."""
        with allure.step("POST /api/posts с пустым content"):
            post_api.create(CreatePostPayload(content=""), status_code=422, success=False)

    @pytest.mark.negative
    @allure.story("Чужие сущности")
    @allure.title("PATCH /api/posts/{id} — редактирование чужого поста запрещено (403)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_foreign_post(self, post_api: PostAPI, post_api_media: PostAPI) -> None:
        """
        Шаги:
        1. Пользователь MEDIA создаёт пост
        2. Пользователь ACTIVE пытается его отредактировать
        3. Автор удаляет свой пост

        Ожидаемый результат: HTTP 403 Forbidden
        """
        foreign = post_api_media.create(CreatePostPayload(**self.gen.post()))

        try:
            with allure.step(f"PATCH /api/posts/{foreign.id} чужим пользователем"):
                post_api.update(
                    str(foreign.id),
                    UpdatePostPayload(content=self.gen.post_content()),
                    status_code=403,
                    success=False,
                )
        finally:
            with allure.step("Автор удаляет свой пост"):
                post_api_media.delete(str(foreign.id))

    @pytest.mark.negative
    @allure.story("Несуществующие сущности")
    @allure.title("GET /api/posts/{id} — несуществующий пост отдаёт 404")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_missing_post(self, post_api: PostAPI) -> None:
        """Ожидаемый результат: HTTP 404 Not Found, а не 500."""
        missing_id = "00000000-0000-0000-0000-000000000000"

        with allure.step(f"GET /api/posts/{missing_id}"):
            post_api.get(missing_id, status_code=404, success=False)
