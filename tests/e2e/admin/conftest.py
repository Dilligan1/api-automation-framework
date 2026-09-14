# Фикстуры сквозного флоу администратора.
# Автор контента — ADMIN, читатель — ACTIVE.

import pytest

from services.comments.api import CommentAPI
from services.likes.api import LikeAPI
from services.notifications.api import NotificationAPI
from services.posts.api import PostAPI


@pytest.fixture(scope="session")
def author_post_api(http_client, token_admin: str) -> PostAPI:
    return PostAPI(http_client, token_admin)


@pytest.fixture(scope="session")
def author_notification_api(http_client, token_admin: str) -> NotificationAPI:
    return NotificationAPI(http_client, token_admin)


@pytest.fixture(scope="session")
def reader_like_api(http_client, token_active: str) -> LikeAPI:
    return LikeAPI(http_client, token_active)


@pytest.fixture(scope="session")
def reader_comment_api(http_client, token_active: str) -> CommentAPI:
    return CommentAPI(http_client, token_active)
