# Эндпоинты администрирования. Доступны ролям admin и moderator —
# разграничение прав проверяется негативными тестами от обычного пользователя.

from config.stages import API_PREFIX


class AdminEndpoints:
    stats = f"{API_PREFIX}/admin/stats"
    users = f"{API_PREFIX}/admin/users"
    posts = f"{API_PREFIX}/admin/posts"

    @staticmethod
    def user(user_id: str) -> str:
        return f"{API_PREFIX}/admin/users/{user_id}"

    @staticmethod
    def post(post_id: str) -> str:
        return f"{API_PREFIX}/admin/posts/{post_id}"
