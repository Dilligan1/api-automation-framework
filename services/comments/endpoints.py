# Эндпоинты комментариев. Вложенность ответов ограничена 3 уровнями.

from config.stages import API_PREFIX


class CommentEndpoints:
    @staticmethod
    def of_post(post_id: str) -> str:
        return f"{API_PREFIX}/posts/{post_id}/comments"

    @staticmethod
    def by_id(comment_id: str) -> str:
        return f"{API_PREFIX}/comments/{comment_id}"

    @staticmethod
    def replies(comment_id: str) -> str:
        return f"{API_PREFIX}/comments/{comment_id}/replies"
