# Провайдер токенов авторизации.
# Знает маппинг .env-ключей для каждого пользователя и кэширует токены,
# чтобы за один прогон pytest каждый пользователь логинился ровно один раз.
#
# Кэш двухуровневый:
#   1. В памяти процесса.
#   2. В файле (.token_cache/<stage>/<user>.json) под FileLock — для pytest-xdist:
#      worker'ы не логинятся независимо, первый пишет токен в файл, остальные
#      читают его же. Кэш очищается мастер-процессом в начале прогона
#      (см. pytest_configure в conftest.py).

import json
import logging
import os
import shutil
from enum import Enum
from pathlib import Path

from filelock import FileLock

from config.stages import API_PREFIX, STAGE

logger = logging.getLogger(__name__)

# Межпроцессный кэш токенов — общий для всех xdist worker'ов
TOKEN_CACHE_DIR = Path(__file__).parent.parent / ".token_cache" / STAGE

LOGIN_ENDPOINT = f"{API_PREFIX}/auth/login"
REFRESH_ENDPOINT = f"{API_PREFIX}/auth/refresh"


def clear_token_cache() -> None:
    """Удалить файловый кэш токенов. Вызывается мастер-процессом перед прогоном."""
    shutil.rmtree(TOKEN_CACHE_DIR, ignore_errors=True)


class User(str, Enum):
    """
    Seed-пользователи песочницы. Значение — префикс env-переменных:
    USERNAME_<VALUE> / PASSWORD_<VALUE>.

    ADMIN      — полный доступ к /api/admin/*
    MODERATOR  — модерация контента
    ACTIVE     — обычный верифицированный пользователь (дефолт в фикстурах)
    MEDIA      — посты с изображениями
    LONGREAD   — длинные тексты (граничные значения по 2000 символов)
    PRIVATE    — приватный аккаунт: подписка уходит в pending
    EMPTY      — новый пользователь без постов (пустые списки, пагинация)
    BANNED     — забанен: ожидаем 403 на защищённых методах
    """

    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"
    ACTIVE = "ACTIVE"
    MEDIA = "MEDIA"
    LONGREAD = "LONGREAD"
    PRIVATE = "PRIVATE"
    EMPTY = "EMPTY"
    BANNED = "BANNED"


class TokenProvider:
    """Выдаёт access-токен пользователя, логинясь не чаще одного раза за прогон."""

    def __init__(self, client) -> None:
        self.client = client
        self._memory_cache: dict[str, dict] = {}

    # -- публичный API ------------------------------------------------------

    def for_user(self, user: User) -> str:
        """Access-токен пользователя (из кэша или свежий логин)."""
        return self._tokens(user)["access_token"]

    def refresh_token_for(self, user: User) -> str:
        """Refresh-токен пользователя — нужен тестам на POST /auth/refresh и /auth/logout."""
        return self._tokens(user)["refresh_token"]

    def credentials(self, user: User) -> tuple[str, str]:
        """Пара (email, password) из .env. Падает явно, если переменных нет."""
        email = os.environ.get(f"EMAIL_{user.value}")
        password = os.environ.get(f"PASSWORD_{user.value}")
        if not email or not password:
            raise RuntimeError(
                f"Не заданы EMAIL_{user.value} / PASSWORD_{user.value} в .env "
                f"(см. .env.example)"
            )
        return email, password

    # -- внутреннее ---------------------------------------------------------

    def _tokens(self, user: User) -> dict:
        if user.value in self._memory_cache:
            return self._memory_cache[user.value]

        TOKEN_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_file = TOKEN_CACHE_DIR / f"{user.value.lower()}.json"

        with FileLock(str(cache_file) + ".lock"):
            if cache_file.exists():
                tokens = json.loads(cache_file.read_text())
            else:
                tokens = self._login(user)
                cache_file.write_text(json.dumps(tokens))

        self._memory_cache[user.value] = tokens
        return tokens

    def _login(self, user: User) -> dict:
        email, password = self.credentials(user)
        logger.info("Логин пользователя %s (%s)", user.value, email)
        response = self.client.post(
            LOGIN_ENDPOINT, json={"email": email, "password": password}
        )
        assert response.status_code == 200, (
            f"Логин {user.value} не удался: HTTP {response.status_code} — "
            f"{response.text[:300]}"
        )
        data = response.json()
        return {
            "access_token": data["access_token"],
            "refresh_token": data["refresh_token"],
        }
