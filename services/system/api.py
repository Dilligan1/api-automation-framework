# Системный сервис: health-check и сброс стенда.
#
# reset() разрушает данные всех пользователей, поэтому вызывается только:
#   - в начале прогона (опционально, через env RESET_BEFORE_RUN=true);
#   - вручную при отладке.
# В параллельном прогоне вызывать reset из теста НЕЛЬЗЯ — уронит соседние worker'ы.

import allure

from services.system.endpoints import SystemEndpoints
from services.system.models.responses import HealthResponse, ResetResponse
from utils.api_helper import APIHelper
from utils.http_client import HTTPClient


class SystemAPI(APIHelper):
    def __init__(self, client: HTTPClient, token: str | None = None) -> None:
        self.client = client
        self.token = token
        self.endpoints = SystemEndpoints()

    @allure.step("Health-check стенда")
    def health(self, **kwargs) -> HealthResponse:
        response = self.client.get(self.endpoints.health)
        return self._validate_response(response, HealthResponse, **kwargs)

    @allure.step("Сброс стенда в исходное состояние")
    def reset(self, **kwargs) -> ResetResponse:
        response = self.client.post(self.endpoints.reset)
        return self._validate_response(response, ResetResponse, **kwargs)
