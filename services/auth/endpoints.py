# Эндпоинты авторизации: регистрация, логин, обновление и отзыв токена.

from config.stages import API_PREFIX


class AuthEndpoints:
    register = f"{API_PREFIX}/auth/register"  # создать пользователя
    login    = f"{API_PREFIX}/auth/login"     # получить access + refresh токены
    refresh  = f"{API_PREFIX}/auth/refresh"   # обменять refresh на новую пару
    logout   = f"{API_PREFIX}/auth/logout"    # отозвать refresh-токен
    me       = f"{API_PREFIX}/auth/me"        # профиль текущего пользователя
