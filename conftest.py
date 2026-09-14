# Корневые фикстуры pytest — session-scoped.
# Каждый пользователь логинится ровно один раз за весь прогон (см. TokenProvider).
#
# Структура:
#   http_client            — общий HTTPClient без авторизации
#   token_provider         — TokenProvider с двухуровневым кэшем токенов
#   token_<user>           — access-токен конкретного seed-пользователя
#   <service>_api          — сервис с дефолтным пользователем (ACTIVE)
#   <service>_api_<user>   — тот же сервис от имени другого пользователя

import os

import pytest
from dotenv import load_dotenv

from auth.token_provider import TokenProvider, User, clear_token_cache
from services.admin.api import AdminAPI
from services.auth.api import AuthAPI
from services.bookmarks.api import BookmarkAPI
from services.comments.api import CommentAPI
from services.follows.api import FollowAPI
from services.likes.api import LikeAPI
from services.messages.api import MessageAPI
from services.notifications.api import NotificationAPI
from services.posts.api import PostAPI
from services.search.api import SearchAPI
from services.system.api import SystemAPI
from services.upload.api import UploadAPI
from services.users.api import UserAPI
from utils.http_client import HTTPClient

load_dotenv()


def pytest_configure(config: pytest.Config) -> None:
    """
    Подготовка прогона. Выполняется только мастер-процессом (не xdist worker'ами):
      - файловый кэш токенов очищается, чтобы прогон начинался со свежего логина,
        а worker'ы делили один токен на пользователя;
      - опционально стенд сбрасывается в исходное состояние (RESET_BEFORE_RUN=true).
    """
    if hasattr(config, "workerinput"):
        return

    clear_token_cache()

    if os.getenv("RESET_BEFORE_RUN", "false").lower() == "true":
        client = HTTPClient()
        try:
            SystemAPI(client).reset()
        finally:
            client.close()


# ---------------------------------------------------------------------------
# HTTP-клиент
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def http_client() -> HTTPClient:
    client = HTTPClient()
    yield client
    client.close()


# ---------------------------------------------------------------------------
# TokenProvider и токены seed-пользователей
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def token_provider(http_client: HTTPClient) -> TokenProvider:
    return TokenProvider(http_client)


@pytest.fixture(scope="session")
def token_active(token_provider: TokenProvider) -> str:
    return token_provider.for_user(User.ACTIVE)


@pytest.fixture(scope="session")
def token_admin(token_provider: TokenProvider) -> str:
    return token_provider.for_user(User.ADMIN)


@pytest.fixture(scope="session")
def token_moderator(token_provider: TokenProvider) -> str:
    return token_provider.for_user(User.MODERATOR)


@pytest.fixture(scope="session")
def token_media(token_provider: TokenProvider) -> str:
    return token_provider.for_user(User.MEDIA)


@pytest.fixture(scope="session")
def token_private(token_provider: TokenProvider) -> str:
    return token_provider.for_user(User.PRIVATE)


@pytest.fixture(scope="session")
def token_empty(token_provider: TokenProvider) -> str:
    return token_provider.for_user(User.EMPTY)


# ---------------------------------------------------------------------------
# Сервисы — дефолтный пользователь (ACTIVE)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def auth_api(http_client: HTTPClient) -> AuthAPI:
    """Без токена: register/login вызываются до авторизации."""
    return AuthAPI(http_client)


@pytest.fixture(scope="session")
def system_api(http_client: HTTPClient) -> SystemAPI:
    return SystemAPI(http_client)


@pytest.fixture(scope="session")
def user_api(http_client: HTTPClient, token_active: str) -> UserAPI:
    return UserAPI(http_client, token_active)


@pytest.fixture(scope="session")
def post_api(http_client: HTTPClient, token_active: str) -> PostAPI:
    return PostAPI(http_client, token_active)


@pytest.fixture(scope="session")
def comment_api(http_client: HTTPClient, token_active: str) -> CommentAPI:
    return CommentAPI(http_client, token_active)


@pytest.fixture(scope="session")
def like_api(http_client: HTTPClient, token_active: str) -> LikeAPI:
    return LikeAPI(http_client, token_active)


@pytest.fixture(scope="session")
def follow_api(http_client: HTTPClient, token_active: str) -> FollowAPI:
    return FollowAPI(http_client, token_active)


@pytest.fixture(scope="session")
def bookmark_api(http_client: HTTPClient, token_active: str) -> BookmarkAPI:
    return BookmarkAPI(http_client, token_active)


@pytest.fixture(scope="session")
def message_api(http_client: HTTPClient, token_active: str) -> MessageAPI:
    return MessageAPI(http_client, token_active)


@pytest.fixture(scope="session")
def notification_api(http_client: HTTPClient, token_active: str) -> NotificationAPI:
    return NotificationAPI(http_client, token_active)


@pytest.fixture(scope="session")
def search_api(http_client: HTTPClient, token_active: str) -> SearchAPI:
    return SearchAPI(http_client, token_active)


@pytest.fixture(scope="session")
def upload_api(http_client: HTTPClient, token_active: str) -> UploadAPI:
    return UploadAPI(http_client, token_active)


# ---------------------------------------------------------------------------
# Сервисы — роли admin / moderator
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def admin_api(http_client: HTTPClient, token_admin: str) -> AdminAPI:
    return AdminAPI(http_client, token_admin)


@pytest.fixture(scope="session")
def admin_api_moderator(http_client: HTTPClient, token_moderator: str) -> AdminAPI:
    return AdminAPI(http_client, token_moderator)


@pytest.fixture(scope="session")
def admin_api_as_user(http_client: HTTPClient, token_active: str) -> AdminAPI:
    """Админские методы от обычного пользователя — для проверки 403."""
    return AdminAPI(http_client, token_active)


# ---------------------------------------------------------------------------
# Сервисы — приватный аккаунт (сценарии follow-request)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def follow_api_private(http_client: HTTPClient, token_private: str) -> FollowAPI:
    return FollowAPI(http_client, token_private)


@pytest.fixture(scope="session")
def post_api_private(http_client: HTTPClient, token_private: str) -> PostAPI:
    return PostAPI(http_client, token_private)


@pytest.fixture(scope="session")
def post_api_media(http_client: HTTPClient, token_media: str) -> PostAPI:
    return PostAPI(http_client, token_media)


# ---------------------------------------------------------------------------
# Функциональные фикстуры — самоочищающиеся сущности
# ---------------------------------------------------------------------------


@pytest.fixture
def registered_users(admin_api: AdminAPI):
    """
    Реестр пользователей, созданных тестом через регистрацию.

    Удалить аккаунт самому пользователю API не позволяет, поэтому уборка идёт
    правами администратора: DELETE /admin/users/{id} деактивирует учётную запись.
    Тест регистрирует пользователя и кладёт его id сюда — фикстура вычистит.
    """
    created: list[str] = []
    yield created
    for user_id in created:
        try:
            admin_api.deactivate_user(user_id)
        except AssertionError:
            pass  # уборка не должна ронять прогон


@pytest.fixture
def created_post(post_api: PostAPI):
    """
    Пост, созданный дефолтным пользователем и удаляемый после теста.

    Тесты не должны оставлять мусор на стенде: стенд общий, а reset
    в параллельном прогоне вызывать нельзя.
    """
    from services.posts.payloads import CreatePostPayload
    from utils.data_generator import DataGenerator

    post = post_api.create(CreatePostPayload(**DataGenerator.post()))
    yield post
    post_api.delete(str(post.id), status_code=204, success=True)
