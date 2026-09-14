# API Automation Framework

[![API tests](https://github.com/Dilligan1/api-automation-framework/actions/workflows/tests.yml/badge.svg)](https://github.com/Dilligan1/api-automation-framework/actions/workflows/tests.yml)
[![Allure report](https://img.shields.io/badge/Allure-отчёт-blue)](https://dilligan1.github.io/api-automation-framework/)

Фреймворк автотестов REST API на **Python + pytest + requests + Pydantic**, построенный по слоистой архитектуре service-object.

Тестируемая система (SUT) — [QA Automation Sandbox](https://github.com/manikosto/qa-automation-sandbox): социальная сеть на FastAPI, 65 эндпоинтов, JWT-авторизация, 8 предустановленных пользователей с разными ролями и состояниями. Поднимается локально одной командой — прогон не зависит от доступности чужих демо-стендов.

> UI-автотесты на ту же систему — в репозитории [ui-automation-framework](https://github.com/Dilligan1/ui-automation-framework).

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

## Как запустить

### Что понадобится

| | |
|---|---|
| Python | 3.11 или новее (`python3 --version`) |
| Docker | с плагином Compose (`docker compose version`) — нужен, чтобы поднять тестируемую систему |
| Git | `git --version` |

Allure CLI ставить необязательно: отчёт можно собрать в контейнере (см. ниже).

### 1. Поднять тестируемую систему

Тесты ходят в [QA Automation Sandbox](https://github.com/manikosto/qa-automation-sandbox) — она поднимается локально, снаружи ничего арендовать не нужно.

```bash
git clone https://github.com/manikosto/qa-automation-sandbox.git
docker compose -f qa-automation-sandbox/docker-compose.yml up -d --build
```

Первая сборка занимает 2–4 минуты. Дождитесь готовности:

```bash
curl http://localhost:8000/api/health
# {"status":"healthy","database":"connected"}
```

Что где живёт: API — `http://localhost:8000` (Swagger на `/docs`), веб-интерфейс — `http://localhost:3000`, база — `localhost:5432`.

### 2. Поставить зависимости

```bash
git clone https://github.com/Dilligan1/api-automation-framework.git
cd api-automation-framework

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Создать `.env`

```bash
cp .env.example .env
```

Файл уже содержит нужные значения по умолчанию — учётные данные seed-пользователей песочницы **публичные** (опубликованы в её README) и одинаковы у всех, так что заполнять вручную ничего не требуется. Достаточно убедиться, что заданы `EMAIL_*` / `PASSWORD_*`; по умолчанию это `alice@buzzhive.com` / `alice123` и т. д.

### 4. Запустить тесты

```bash
pytest                    # всё, что есть — около 20 секунд
```

Отдельные наборы:

```bash
pytest -m smoke           # базовая работоспособность каждого сервиса
pytest -m negative        # коды ошибок, границы, разграничение прав
pytest -m e2e             # сквозные сценарии по ролям
pytest -m critical        # только бизнес-критичные проверки
```

Параллельно и точечно:

```bash
pytest -n 4                                   # в 4 процесса
pytest tests/smoke/test_posts.py              # один файл
pytest -k "login"                             # по части имени теста
pytest -v --tb=long                           # подробный вывод и трейсбеки
```

### 5. Посмотреть отчёт

```bash
pytest --alluredir=allure-results
allure serve allure-results          # если Allure CLI установлен
```

Без установки Allure CLI — собрать отчёт в контейнере:

```bash
docker compose run --rm report
open allure-report/index.html        # Linux: xdg-open
```

В отчёт попадают URL, тело запроса и тело ответа каждого вызова, а также шаги сервиса и шаги теста.

### Вариант без установки Python

Весь прогон целиком в контейнере:

```bash
docker compose run --rm smoke
docker compose run --rm negative
docker compose run --rm e2e
docker compose run --rm report
```

### Если что-то пошло не так

| Симптом | Причина и что делать |
|---|---|
| `Connection refused` на `localhost:8000` | Песочница не поднялась. `docker compose -f qa-automation-sandbox/docker-compose.yml logs backend` |
| `port is already allocated` | Порты 8000/3000/5432 заняты другим процессом — освободите их или измените порты в compose песочницы и хосты в `.env` |
| `RuntimeError: Не заданы EMAIL_… / PASSWORD_…` | Нет `.env` — вернитесь к шагу 3 |
| Тест `test_refresh_issues_new_pair` помечен `xfail` | Это известный дефект приложения, не поломка тестов — разбор в [docs/known-issues.md](docs/known-issues.md) |
| Данные на стенде «разъехались» | Сбросить к исходному состоянию: `curl -X POST http://localhost:8000/api/reset` |

Погасить стенд, когда закончили:

```bash
docker compose -f qa-automation-sandbox/docker-compose.yml down -v
```

### Как это гоняется в CI

То же самое делает GitHub Actions на каждый push, PR и по расписанию ночью: поднимает песочницу на раннере, ждёт готовности, гоняет тесты в 4 процесса и публикует отчёт. Постоянно работающий стенд не нужен — смотрите [`.github/workflows/tests.yml`](.github/workflows/tests.yml).

## Отчётность

Каждый запрос попадает в Allure: URL, тело запроса, тело ответа, шаги сервиса и шаги теста. В CI отчёт публикуется на GitHub Pages — [посмотреть последний прогон](https://dilligan1.github.io/api-automation-framework/).

## Документация

- [docs/architecture.md](docs/architecture.md) — слои и границы ответственности
- [docs/api_map.md](docs/api_map.md) — карта эндпоинтов по сервисам
- [docs/test-plan.md](docs/test-plan.md) — уровни тестирования и что где проверяется
- [docs/status_machine.md](docs/status_machine.md) — статусные модели сущностей
- [docs/known-issues.md](docs/known-issues.md) — найденный дефект приложения и почему один тест в карантине
