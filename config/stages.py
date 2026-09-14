# Конфигурация стендов. Активный стенд выбирается переменной окружения STAGE.
#
# local  — песочница, поднятая локально через docker compose
# ci     — тот же контейнер внутри GitHub Actions (service container)
#
# Все хосты переопределяются через env, чтобы не править код под чужой стенд.

import os
from typing import TypedDict

from dotenv import load_dotenv

load_dotenv()


class StageConfig(TypedDict):
    api: str
    ui: str


STAGES: dict[str, StageConfig] = {
    "local": {
        "api": "http://localhost:8000",
        "ui": "http://localhost:3000",
    },
    "ci": {
        "api": "http://backend:8000",
        "ui": "http://frontend:3000",
    },
}

STAGE = os.getenv("STAGE", "local")

# Env HOST_<STAGE> имеет приоритет над дефолтом из STAGES
HOST = os.getenv(f"API_HOST_{STAGE.upper()}", STAGES[STAGE]["api"])
API_PREFIX = f"{HOST}/api"
UI_HOST = os.getenv(f"UI_HOST_{STAGE.upper()}", STAGES[STAGE]["ui"])
