# HTTP-клиент на основе requests.Session.
# Транспортный слой: все сервисные классы получают экземпляр HTTPClient через
# фикстуру и ходят в сеть только через него.
# Автоматически логирует каждый запрос и прикрепляет URL/тело в Allure-отчёт.

import json
import logging

import allure
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

# При 429/5xx urllib3 делает до 5 повторных попыток с экспоненциальным backoff:
# 1s, 2s, 4s, 8s, 16s. Если сервер отдаёт Retry-After — уважает его.
_RETRY_STRATEGY = Retry(
    total=5,
    status_forcelist=[429, 502, 503, 504],
    allowed_methods=False,  # retry на всех методах, включая POST
    backoff_factor=1,
    respect_retry_after_header=True,
    raise_on_status=False,
)


class HTTPClient:
    """Одна сессия на весь прогон pytest (фикстура scope="session")."""

    def __init__(self, timeout: float = 30.0) -> None:
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        adapter = HTTPAdapter(max_retries=_RETRY_STRATEGY)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def get(self, url: str, **kwargs) -> requests.Response:
        return self._request("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        return self._request("POST", url, **kwargs)

    def patch(self, url: str, **kwargs) -> requests.Response:
        return self._request("PATCH", url, **kwargs)

    def delete(self, url: str, **kwargs) -> requests.Response:
        return self._request("DELETE", url, **kwargs)

    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        response = self.session.request(method, url, timeout=self.timeout, **kwargs)
        self._log(method, url, response)
        self._attach_request(response)
        return response

    def _log(self, method: str, url: str, response: requests.Response) -> None:
        logger.info("%s %s -> %s", method, url, response.status_code)

    def _attach_request(self, response: requests.Response) -> None:
        allure.attach(str(response.url), "URL", allure.attachment_type.TEXT)
        if not response.request.body:
            return
        raw = (
            response.request.body
            if isinstance(response.request.body, str)
            else response.request.body.decode("utf-8", errors="replace")
        )
        try:
            body = json.dumps(json.loads(raw), ensure_ascii=False, indent=2)
        except (ValueError, TypeError):
            body = raw
        allure.attach(body, "Request Body", allure.attachment_type.JSON)

    def close(self) -> None:
        self.session.close()
