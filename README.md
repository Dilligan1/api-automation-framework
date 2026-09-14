# API Automation Framework

Фреймворк автотестов REST API на **Python + pytest + requests + Pydantic**, построенный по слоистой архитектуре service-object.

Тестируемая система (SUT) — [QA Automation Sandbox](https://github.com/manikosto/qa-automation-sandbox): социальная сеть на FastAPI, 65 эндпоинтов, JWT-авторизация, 8 предустановленных пользователей с разными ролями и состояниями. Поднимается локально одной командой — прогон не зависит от доступности чужих демо-стендов.

> UI-автотесты на ту же систему — в репозитории [ui-automation-framework](../ui-automation-framework).

---

## Что демонстрирует проект

| Задача | Решение в коде |
|---|---|
| Единая точка сетевого ввода-вывода | `utils/http_client.py` — одна `requests.Session` на прогон, retry на 429/5xx с экспоненциальным backoff и `Retry-After`, авто-вложения в Allure |
| Проверка контракта, а не только кода ответа | `utils/api_helper.py` + Pydantic-модели: каждый ответ десериализуется в схему, расхождение падает с читаемым телом ответа |
| Один логин на пользователя за прогон | `auth/token_provider.py` — двухуровневый кэш токенов (память + файл под `FileLock`), безопасный для `pytest-xdist` |
| Изоляция доменов | `services/<domain>/{api,endpoints,payloads,models}` — 13 сервисов, ни один тест не собирает URL руками |
| Негативные сценарии без дублирования кода | тот же метод сервиса с `status_code=403, success=False` |
| Состояния, недостижимые через API | `utils/db_handler.py` — прямой доступ к PostgreSQL (окно редактирования, soft delete, сверка счётчиков) |
| Повторяемость прогона | `DataGenerator` для всех входных данных, самоочищающиеся фикстуры, `POST /api/reset` перед прогоном |

## Архитектура

```
conftest.py                 session-scoped фикстуры: клиент, токены, сервисы
config/
  stages.py                 хосты стендов, выбор по STAGE
  base_test.py              BaseTest — общий предок всех тест-классов
  test_data.py              seed-пользователи и границы бэкенда
  headers.py, db_config.py
auth/
  token_provider.py         логин и кэш токенов (xdist-safe)
services/
  <domain>/api.py           методы сервиса, каждый под @allure.step
  <domain>/endpoints.py     URL, собранные из HOST
  <domain>/payloads.py      Pydantic-модели запросов
  <domain>/models/          Pydantic-модели ответов
  common/models/            PaginatedResponse, UserBrief, PostResponse
utils/
  http_client.py            транспорт
  api_helper.py             валидация ответа + Allure
  data_generator.py         фабрика тестовых данных
  db_handler.py             прямой доступ к БД стенда
tests/
  smoke/                    каждый метод отвечает (быстрый прогон)
  negative/                 коды ошибок, границы, разграничение прав
  regression/               широкое покрытие вариаций
  e2e/base_flow.py          сквозной флоу, один тест на пользователя
  e2e/<user>/               привязка флоу к конкретной роли
```

Поток вызова: `тест → <Domain>API → HTTPClient → SUT` и обратно `response → APIHelper._validate_response → Pydantic-модель → assert в тесте`.

## Быстрый старт

```bash
# 1. Поднять тестируемую систему
git clone https://github.com/manikosto/qa-automation-sandbox.git
docker compose -f qa-automation-sandbox/docker-compose.yml up -d

# 2. Настроить окружение
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # заполнить учётные данные seed-пользователей

# 3. Прогон
pytest -m smoke -n 4
```

### Полезные команды

```bash
pytest -m smoke                  # быстрый прогон
pytest -m negative               # негативные сценарии
pytest -m e2e                    # сквозные флоу по ролям
pytest -n 4                      # параллельно (xdist)
pytest --alluredir=allure-results && allure serve allure-results

docker compose run --rm smoke    # то же в контейнере
docker compose run --rm report   # HTML-отчёт Allure
```

## Отчётность

Каждый запрос попадает в Allure: URL, тело запроса, тело ответа, шаги сервиса и шаги теста. В CI отчёт публикуется на GitHub Pages (`.github/workflows/tests.yml`).

## Документация

- [docs/architecture.md](docs/architecture.md) — слои и границы ответственности
- [docs/api_map.md](docs/api_map.md) — карта эндпоинтов по сервисам
- [docs/test-plan.md](docs/test-plan.md) — уровни тестирования и что где проверяется
- [docs/status_machine.md](docs/status_machine.md) — статусные модели сущностей
