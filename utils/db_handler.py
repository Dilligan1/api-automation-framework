# Прямой доступ к БД стенда.
# Нужен там, где состояние через API не воспроизвести:
#   - «состарить» пост, чтобы выйти за 15-минутное окно редактирования;
#   - проверить soft delete (is_deleted) — API такие записи не отдаёт;
#   - сверить денормализованные счётчики (likes_count, followers_count).
#
# Контекстный менеджер: соединение закрывается даже если тест упал.

import logging
from contextlib import contextmanager
from typing import Any

import psycopg2
from psycopg2.extras import RealDictCursor

from config.db_config import DBConfig

logger = logging.getLogger(__name__)


class DatabaseHandler:
    def __init__(self, config: DBConfig) -> None:
        self.config = config
        self.connection = None
        self.cursor = None

    def connect(self) -> "DatabaseHandler":
        if self.config.db_name != "postgres":
            raise ValueError("Поддерживается только PostgreSQL")
        self.connection = psycopg2.connect(
            host=self.config.server,
            port=self.config.port,
            dbname=self.config.database,
            user=self.config.username,
            password=self.config.password,
        )
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        return self

    # -- чтение -------------------------------------------------------------

    def fetch_one(self, query: str, params: tuple = ()) -> dict[str, Any] | None:
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query: str, params: tuple = ()) -> list[dict[str, Any]]:
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    # -- запись -------------------------------------------------------------

    def execute(self, query: str, params: tuple = ()) -> int:
        """Выполнить запрос с коммитом. Возвращает число затронутых строк."""
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor.rowcount

    # -- доменные помощники -------------------------------------------------

    def age_post(self, post_id: str, minutes: int) -> int:
        """Сдвинуть created_at поста в прошлое — закрыть окно редактирования."""
        return self.execute(
            "UPDATE posts SET created_at = created_at - make_interval(mins => %s) "
            "WHERE id = %s",
            (minutes, post_id),
        )

    def is_soft_deleted(self, post_id: str) -> bool:
        row = self.fetch_one("SELECT is_deleted FROM posts WHERE id = %s", (post_id,))
        assert row is not None, f"Пост {post_id} не найден в БД"
        return bool(row["is_deleted"])

    def close(self) -> None:
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


@contextmanager
def database(config: DBConfig):
    """with database(DB_CONFIG) as db: db.age_post(...)"""
    handler = DatabaseHandler(config).connect()
    try:
        yield handler
    finally:
        handler.close()
