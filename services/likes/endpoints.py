# Эндпоинты реакций. Шесть типов: like, love, laugh, wow, sad, angry.

from config.stages import API_PREFIX


class LikeEndpoints:
    @staticmethod
    def post_like(post_id: str) -> str:
        return f"{API_PREFIX}/posts/{post_id}/like"

    @staticmethod
    def post_likes(post_id: str) -> str:
        return f"{API_PREFIX}/posts/{post_id}/likes"

    @staticmethod
    def comment_like(comment_id: str) -> str:
        return f"{API_PREFIX}/comments/{comment_id}/like"
