# Параметры подключения к БД стенда.
# Прямой доступ к базе нужен там, где состояние через API не воспроизвести:
# просроченное окно редактирования поста, soft-deleted записи, счётчики.
# Выбирается автоматически по текущему STAGE.

import os
from dataclasses import dataclass

from config.stages import STAGE


@dataclass(frozen=True)
class DBConfig:
    db_name: str
    server: str
    port: int
    database: str
    username: str
    password: str


DB_CONFIG = DBConfig(
    db_name="postgres",
    server=os.getenv(f"DB_HOST_{STAGE.upper()}", "localhost"),
    port=int(os.getenv(f"DB_PORT_{STAGE.upper()}", "5432")),
    database=os.getenv(f"DB_NAME_{STAGE.upper()}", "sandbox"),
    username=os.getenv(f"DB_USER_{STAGE.upper()}", "sandbox"),
    password=os.getenv(f"DB_PASSWORD_{STAGE.upper()}", "sandbox"),
)
