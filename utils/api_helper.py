# Базовый класс для всех сервисных API-классов.
# Предоставляет:
#   - attach_response  — прикрепляет JSON-ответ в Allure-отчёт
#   - _validate_response — проверяет статус-код и десериализует ответ в Pydantic-модель
#   - _auth_headers    — заголовок Authorization: Bearer <token>
#
# Использование:
#   class AuthAPI(APIHelper):
#       def login(self, email, password) -> TokenResponse:
#           response = self.client.post(AuthEndpoints.login, json={...})
#           return self._validate_response(response, TokenResponse)

import json
from typing import TypeVar

import allure
import requests
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class APIHelper:
    client = None
    token: str | None = None

    @property
    def _auth_headers(self) -> dict[str, str]:
        """Bearer-заголовок текущего пользователя сервиса."""
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def attach_response(self, response: requests.Response) -> None:
        """Прикрепить ответ в Allure-отчёт."""
        if not response.content:
            allure.attach(
                body=f"HTTP {response.status_code} — empty body",
                name="API Response",
                attachment_type=allure.attachment_type.TEXT,
            )
            return
        try:
            body = json.dumps(response.json(), indent=4, ensure_ascii=False)
            attachment_type = allure.attachment_type.JSON
        except ValueError:
            body = response.text
            attachment_type = allure.attachment_type.TEXT
        allure.attach(body=body, name="API Response", attachment_type=attachment_type)

    def _validate_response(
        self,
        response: requests.Response,
        model: type[T] | None,
        status_code: int = 200,
        success: bool = True,
    ) -> T | list[T] | None:
        """
        Проверить ответ и десериализовать в Pydantic-модель.

        success=True  — позитивный сценарий: проверяем ожидаемый status_code,
                        возвращаем модель (или список моделей). model=None —
                        для 204 No Content, где тела нет.
        success=False — негативный сценарий: проверяем, что статус совпадает
                        с ожидаемым кодом ошибки, возвращаем None.
        """
        self.attach_response(response)

        assert response.status_code == status_code, (
            f"Ожидался статус {status_code}, получен {response.status_code}: "
            f"{response.text[:300]}"
        )

        if not success or model is None:
            return None

        data = response.json()
        if isinstance(data, list):
            return [model.model_validate(item) for item in data]
        try:
            return model.model_validate(data)
        except Exception as e:
            readable = json.dumps(data, ensure_ascii=False, indent=2)
            raise AssertionError(
                f"Pydantic validation failed.\nResponse body:\n{readable}"
            ) from e
