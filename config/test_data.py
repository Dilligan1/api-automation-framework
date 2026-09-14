# Статические тестовые данные стенда.
#
# Песочница сидируется фиксированным набором данных (POST /api/reset возвращает
# его в исходное состояние), поэтому seed-пользователи и их состояния известны
# заранее и вынесены сюда, а не размазаны по тестам.

import os

from config.stages import STAGE

# ---------------------------------------------------------------------------
# Seed-пользователи песочницы (пароли — дефолтные, не секреты, но берутся из env)
# ---------------------------------------------------------------------------

SEED_DOMAIN = os.getenv("SEED_DOMAIN", "buzzhive.com")

# Хэндлы seed-пользователей — используются в путях /users/{username}/...
USERNAME_ADMIN = os.getenv("USERNAME_ADMIN", "admin")
USERNAME_MODERATOR = os.getenv("USERNAME_MODERATOR", "moderator")
USERNAME_ACTIVE = os.getenv("USERNAME_ACTIVE", "alice_dev")
USERNAME_MEDIA = os.getenv("USERNAME_MEDIA", "bob_photo")
USERNAME_LONGREAD = os.getenv("USERNAME_LONGREAD", "carol_writes")
USERNAME_PRIVATE = os.getenv("USERNAME_PRIVATE", "dave_quiet")
USERNAME_EMPTY = os.getenv("USERNAME_EMPTY", "eve_new")
USERNAME_BANNED = os.getenv("USERNAME_BANNED", "frank_banned")

# ---------------------------------------------------------------------------
# Ограничения бэкенда — источник границ для regression/negative-тестов
# ---------------------------------------------------------------------------

POST_CONTENT_MAX = 2000        # символов в теле поста
COMMENT_CONTENT_MAX = 1000     # символов в комментарии
MESSAGE_CONTENT_MAX = 2000     # символов в сообщении
COMMENT_DEPTH_MAX = 3          # уровней вложенности ответов
POST_EDIT_WINDOW_MINUTES = 15  # окно редактирования поста
UPLOAD_MAX_BYTES = 5 * 1024 * 1024
UPLOAD_ALLOWED_TYPES = ("image/jpeg", "image/png", "image/gif", "image/webp")
REACTIONS = ("like", "love", "laugh", "wow", "sad", "angry")
PER_PAGE_MAX = 100

# ---------------------------------------------------------------------------
# Fixture-сущности стенда (при необходимости закрепить ID вручную)
# ---------------------------------------------------------------------------

FIXTURE_POST_ID = os.getenv(f"FIXTURE_POST_ID_{STAGE.upper()}")
FIXTURE_CONVERSATION_ID = os.getenv(f"FIXTURE_CONVERSATION_ID_{STAGE.upper()}")
