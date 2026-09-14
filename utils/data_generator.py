"""
DataGenerator — фабрика тестовых данных.
НИКОГДА не хардкодить email, пароли, тексты постов и имена в тестах:
параллельный прогон и повторный запуск на том же стенде должны быть безопасны.
"""

import base64
from typing import Any

from faker import Faker

fake = Faker("en_US")


class DataGenerator:
    """Factory for generating test data. NEVER hardcode values in tests."""

    # === Пользователи ===

    @staticmethod
    def user(**overrides) -> dict[str, Any]:
        """Данные для POST /api/auth/register."""
        data = {
            "email": DataGenerator.unique_email(),
            "username": DataGenerator.unique_username(),
            "password": fake.password(length=12),
            "display_name": fake.name(),
        }
        data.update(overrides)
        return data

    @staticmethod
    def unique_email(prefix: str = "qa", domain: str = "example.com") -> str:
        return f"{prefix}+{fake.uuid4()[:8]}@{domain}"

    @staticmethod
    def unique_username(prefix: str = "qa") -> str:
        """username бэкенда: ^[a-zA-Z0-9_]+$, 3-30 символов."""
        return f"{prefix}_{fake.uuid4()[:8]}"

    # === Контент ===

    @staticmethod
    def post(**overrides) -> dict[str, Any]:
        """Тело POST /api/posts."""
        data = {"content": DataGenerator.post_content(), "visibility": "public"}
        data.update(overrides)
        return data

    @staticmethod
    def post_content(words: int = 12, hashtags: int = 1) -> str:
        text = fake.sentence(nb_words=words)
        tags = " ".join(f"#{fake.word()}{fake.random_number(digits=4)}" for _ in range(hashtags))
        return f"{text} {tags}".strip()

    @staticmethod
    def text_of_length(length: int) -> str:
        """Строка ровно заданной длины — для проверки границ (2000 символов)."""
        return fake.pystr(min_chars=length, max_chars=length)

    @staticmethod
    def comment_text() -> str:
        return fake.sentence(nb_words=8)

    @staticmethod
    def message_text() -> str:
        return fake.sentence(nb_words=6)

    # === Файлы ===

    @staticmethod
    def png_bytes() -> bytes:
        """Минимальный валидный PNG 1x1 — для POST /api/upload/image."""
        return base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
        )

    @staticmethod
    def oversized_bytes(size: int) -> bytes:
        """Буфер заданного размера — для проверки лимита 5 MB."""
        return b"\x00" * size
