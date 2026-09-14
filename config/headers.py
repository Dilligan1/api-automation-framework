# HTTP-заголовки проекта.
# Content-Type: application/json выставляется глобально в HTTPClient.session,
# Authorization: Bearer собирается в APIHelper._auth_headers.

# Сбрасывает Content-Type для multipart/form-data (загрузка изображений):
# requests сам выставит правильный Content-Type с boundary при наличии files=.
MULTIPART_OVERRIDE: dict[str, None] = {"Content-Type": None}

# Язык интерфейса — бэкенд отдаёт локализованные тексты ошибок
ACCEPT_LANGUAGE_EN: dict[str, str] = {"Accept-Language": "en"}
