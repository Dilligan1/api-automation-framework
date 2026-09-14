# Фикстуры сквозного флоу для пользователя ACTIVE.
# Автор — ACTIVE, читатель — MEDIA: взаимодействие должно идти между разными
# аккаунтами, иначе уведомления себе не создаются.

import pytest

from services.comments.api import CommentAPI
from services.likes.api import LikeAPI
from services.notifications.api import NotificationAPI
from services.posts.api import PostAPI


@pytest.fixture(scope="session")
def author_post_api(http_client, token_active: str) -> PostAPI:
    return PostAPI(http_client, token_active)


@pytest.fixture(scope="session")
def author_notification_api(http_client, token_active: str) -> NotificationAPI:
    return NotificationAPI(http_client, token_active)


@pytest.fixture(scope="session")
def reader_like_api(http_client, token_media: str) -> LikeAPI:
    return LikeAPI(http_client, token_media)


@pytest.fixture(scope="session")
def reader_comment_api(http_client, token_media: str) -> CommentAPI:
    return CommentAPI(http_client, token_media)
