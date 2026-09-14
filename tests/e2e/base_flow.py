# Базовый класс сквозного (E2E) флоу.
# Не собирается pytest напрямую — только через подклассы в папках пользователей
# (tests/e2e/<user>/test_full_flow.py).
#
# E2E = ОДИН тест на пользователя: весь бизнес-путь выполняется последовательно
# внутри одного метода, этапы — через `with allure.step(...)`. Состояние — ЛОКАЛЬНЫЕ
# переменные, без переменных класса: тест самодостаточен и параллельно-безопасен.
# (Гранулярное покрытие отдельных методов — в tests/smoke/; широкий регресс —
# в tests/regression/.)
#
# Новые этапы добавляются как новые allure.step ВНУТРИ test_full_flow,
# а не как отдельные тест-методы.

from __future__ import annotations

import allure
import pytest

from config.base_test import BaseTest
from services.comments.api import CommentAPI
from services.comments.payloads import CreateCommentPayload
from services.likes.api import LikeAPI
from services.likes.payloads import ReactionPayload
from services.notifications.api import NotificationAPI
from services.posts.api import PostAPI
from services.posts.payloads import CreatePostPayload, UpdatePostPayload


class BaseFlow(BaseTest):
    """
    Сквозной путь пользователя: публикация поста → реакция → комментарий →
    уведомление автору → редактирование → удаление.

    Подкласс обязан получить из conftest.py своей папки четыре фикстуры:
        author_post_api, author_notification_api,
        reader_like_api, reader_comment_api
    За счёт этого один и тот же флоу прогоняется от разных ролей.

    Объявлять их здесь заглушками нельзя: фикстура, определённая в классе,
    перекрывает одноимённую из conftest.py, и подкласс её уже не переопределит.
    """

    @pytest.mark.e2e
    @pytest.mark.critical
    @allure.severity(allure.severity_level.BLOCKER)
    def test_full_flow(
        self,
        author_post_api: PostAPI,
        reader_like_api: LikeAPI,
        reader_comment_api: CommentAPI,
        author_notification_api: NotificationAPI,
    ) -> None:
        """
        Сквозной сценарий социального взаимодействия.

        Шаги:
        1. Автор публикует пост
        2. Читатель ставит реакцию
        3. Читатель комментирует пост
        4. Автор видит рост счётчиков на своём посте
        5. Автору приходит уведомление
        6. Автор редактирует пост (в пределах 15-минутного окна)
        7. Автор удаляет пост — стенд остаётся чистым

        Ожидаемый результат: каждый этап отрабатывает штатно,
        счётчики и уведомления консистентны действиям читателя.
        """
        with allure.step("1. Автор публикует пост"):
            payload = CreatePostPayload(**self.gen.post())
            post = author_post_api.create(payload)
            post_id = str(post.id)
            allure.attach(post_id, "post_id", allure.attachment_type.TEXT)

        try:
            with allure.step("2. Читатель ставит реакцию на пост"):
                like = reader_like_api.like_post(post_id, ReactionPayload(reaction="love"))
                assert like.reaction == "love", (
                    f"Сохранён не тот тип реакции: {like.reaction}"
                )

            with allure.step("3. Читатель комментирует пост"):
                comment = reader_comment_api.create(
                    post_id, CreateCommentPayload(content=self.gen.comment_text())
                )
                assert comment.post_id == post.id, "Комментарий привязан к другому посту"

            with allure.step("4. Автор видит обновлённые счётчики поста"):
                refreshed = author_post_api.get(post_id)
                assert refreshed.likes_count == 1, (
                    f"Ожидался 1 лайк, в карточке {refreshed.likes_count}"
                )
                assert refreshed.comments_count == 1, (
                    f"Ожидался 1 комментарий, в карточке {refreshed.comments_count}"
                )

            with allure.step("5. Автору приходит уведомление о взаимодействии"):
                notifications = author_notification_api.list_notifications()
                types = {n.type for n in notifications.items}
                assert types & {"like", "comment"}, (
                    f"Уведомлений о лайке/комментарии нет. Пришли типы: {types or '—'}"
                )

            with allure.step("6. Автор редактирует пост в окне редактирования"):
                new_content = self.gen.post_content()
                edited = author_post_api.update(
                    post_id, UpdatePostPayload(content=new_content)
                )
                assert edited.content == new_content, "Текст поста не обновился"

        finally:
            with allure.step("7. Автор удаляет пост — стенд остаётся чистым"):
                author_post_api.delete(post_id)
