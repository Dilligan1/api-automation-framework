# Фикстуры сквозного флоу для приватного аккаунта.
# Автор — PRIVATE, читатель — ACTIVE.
# Особенность аккаунта: подписка на него создаётся в статусе pending
# и требует подтверждения владельцем (см. test_private_follow_flow.py).

import pytest

from services.comments.api import CommentAPI
from services.likes.api import LikeAPI
from services.notifications.api import NotificationAPI
from services.posts.api import PostAPI


@pytest.fixture(scope="session")
def author_post_api(http_client, token_private: str) -> PostAPI:
    return PostAPI(http_client, token_private)


@pytest.fixture(scope="session")
def author_notification_api(http_client, token_private: str) -> NotificationAPI:
    return NotificationAPI(http_client, token_private)


@pytest.fixture(scope="session")
def reader_like_api(http_client, token_active: str) -> LikeAPI:
    return LikeAPI(http_client, token_active)


@pytest.fixture(scope="session")
def reader_comment_api(http_client, token_active: str) -> CommentAPI:
    return CommentAPI(http_client, token_active)
