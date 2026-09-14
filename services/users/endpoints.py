# Эндпоинты пользователей: список, профиль, редактирование, аватар, связи.

from config.stages import API_PREFIX


class UserEndpoints:
    list_users  = f"{API_PREFIX}/users"
    suggestions = f"{API_PREFIX}/users/suggestions"
    update_me   = f"{API_PREFIX}/users/me"
    avatar      = f"{API_PREFIX}/users/me/avatar"

    @staticmethod
    def by_username(username: str) -> str:
        return f"{API_PREFIX}/users/{username}"

    @staticmethod
    def posts(username: str) -> str:
        return f"{API_PREFIX}/users/{username}/posts"

    @staticmethod
    def followers(username: str) -> str:
        return f"{API_PREFIX}/users/{username}/followers"

    @staticmethod
    def following(username: str) -> str:
        return f"{API_PREFIX}/users/{username}/following"
