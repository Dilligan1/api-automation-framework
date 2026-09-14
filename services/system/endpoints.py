# Системные эндпоинты: health-check и сброс стенда в исходное состояние.

from config.stages import API_PREFIX


class SystemEndpoints:
    health = f"{API_PREFIX}/health"
    reset  = f"{API_PREFIX}/reset"
