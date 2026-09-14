# Карта API

Базовый префикс: `{HOST}/api`. Хост задаётся `config/stages.py`.

## Auth — `services/auth`
| Метод | Эндпоинт | Назначение |
|---|---|---|
| POST | `/auth/register` | Регистрация пользователя |
| POST | `/auth/login` | Выдача пары access + refresh |
| POST | `/auth/refresh` | Обмен refresh на новую пару |
| POST | `/auth/logout` | Отзыв refresh-токена |
| GET | `/auth/me` | Профиль владельца токена |

## Users — `services/users`
| Метод | Эндпоинт | Назначение |
|---|---|---|
| GET | `/users` | Каталог пользователей |
| GET | `/users/suggestions` | Рекомендации к подписке |
| GET | `/users/{username}` | Профиль |
| PATCH | `/users/me` | Изменение своего профиля |
| POST/DELETE | `/users/me/avatar` | Загрузка и удаление аватара |
| GET | `/users/{username}/posts` | Посты пользователя |
| GET | `/users/{username}/followers` | Подписчики |
| GET | `/users/{username}/following` | Подписки |

## Follows — `services/follows`
| Метод | Эндпоинт | Назначение |
|---|---|---|
| POST/DELETE | `/users/{username}/follow` | Подписка и отписка |
| GET | `/follows/requests` | Входящие запросы (приватный аккаунт) |
| POST | `/follows/requests/{id}/accept` | Подтверждение запроса |
| POST | `/follows/requests/{id}/reject` | Отклонение запроса |

## Posts — `services/posts`
| Метод | Эндпоинт | Назначение |
|---|---|---|
| GET | `/posts` | Все посты |
| GET | `/posts/feed` | Персональная лента |
| POST | `/posts` | Создание поста |
| GET/PATCH/DELETE | `/posts/{id}` | Чтение, правка, удаление |
| POST | `/posts/{id}/repost` | Репост или цитата |
| POST/DELETE | `/posts/{id}/pin` | Закрепление |

## Comments — `services/comments`
| Метод | Эндпоинт | Назначение |
|---|---|---|
| GET/POST | `/posts/{post_id}/comments` | Комментарии поста |
| PATCH/DELETE | `/comments/{id}` | Правка и удаление |
| GET/POST | `/comments/{id}/replies` | Ответы (до 3 уровней) |

## Likes — `services/likes`
| Метод | Эндпоинт | Назначение |
|---|---|---|
| POST/DELETE | `/posts/{id}/like` | Реакция на пост |
| GET | `/posts/{id}/likes` | Кто отреагировал |
| POST/DELETE | `/comments/{id}/like` | Реакция на комментарий |

## Bookmarks — `services/bookmarks`
| Метод | Эндпоинт | Назначение |
|---|---|---|
| GET | `/bookmarks` | Список закладок |
| POST/DELETE | `/posts/{id}/bookmark` | Добавить и убрать |

## Messages — `services/messages`
| Метод | Эндпоинт | Назначение |
|---|---|---|
| GET/POST | `/conversations` | Диалоги |
| POST | `/conversations/dm/{username}` | Найти или создать 1:1 |
| GET | `/conversations/{id}` | Карточка диалога |
| GET/POST | `/conversations/{id}/messages` | Сообщения |
| POST | `/conversations/{id}/read` | Отметить прочитанным |
| DELETE | `/messages/{id}` | Удаление сообщения |

## Notifications — `services/notifications`
| Метод | Эндпоинт | Назначение |
|---|---|---|
| GET | `/notifications` | Список |
| GET | `/notifications/unread-count` | Счётчик непрочитанных |
| POST | `/notifications/{id}/read` | Отметить одно |
| POST | `/notifications/read-all` | Отметить все |

## Search — `services/search`
| Метод | Эндпоинт | Назначение |
|---|---|---|
| GET | `/search/users` | Поиск пользователей |
| GET | `/search/posts` | Поиск постов |
| GET | `/search/hashtags` | Поиск хэштегов |
| GET | `/search/trending/hashtags` | Тренды |

## Admin — `services/admin`
| Метод | Эндпоинт | Назначение |
|---|---|---|
| GET | `/admin/stats` | Статистика дашборда |
| GET | `/admin/users` | Все пользователи |
| PATCH | `/admin/users/{id}` | Роль, бан, верификация |
| DELETE | `/admin/users/{id}` | Деактивация |
| GET | `/admin/posts` | Все посты |
| DELETE | `/admin/posts/{id}` | Модераторское удаление |

## Upload / System
| Метод | Эндпоинт | Назначение |
|---|---|---|
| POST | `/upload/image` | Загрузка изображения (≤ 5 MB) |
| GET | `/health` | Health-check |
| POST | `/reset` | Сброс стенда к seed-данным |
