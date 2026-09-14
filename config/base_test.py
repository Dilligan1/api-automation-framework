# Базовый класс для всех тест-классов проекта.
# Наследование от BaseTest обязательно — bare def test_*() запрещены.
# Предоставляет:
#   self.client — HTTPClient (shared session)
#   self.gen    — DataGenerator (фабрика тестовых данных)
# API-сервисы (posts_api, admin_api и т.д.) запрашиваются явно
# через параметры тест-методов из conftest.py.

import pytest

from utils.data_generator import DataGenerator
from utils.http_client import HTTPClient


class BaseTest:
    client: HTTPClient
    gen: DataGenerator

    @pytest.fixture(autouse=True)
    def _setup_base(self, http_client: HTTPClient) -> None:
        self.client = http_client
        self.gen = DataGenerator()
