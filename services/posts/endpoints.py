# Эндпоинты постов: лента, CRUD, репост и закрепление.

from config.stages import API_PREFIX


class PostEndpoints:
    posts = f"{API_PREFIX}/posts"           # GET список / POST создать
    feed  = f"{API_PREFIX}/posts/feed"      # персональная лента подписок

    @staticmethod
    def by_id(post_id: str) -> str:
        return f"{API_PREFIX}/posts/{post_id}"

    @staticmethod
    def repost(post_id: str) -> str:
        return f"{API_PREFIX}/posts/{post_id}/repost"

    @staticmethod
    def pin(post_id: str) -> str:
        return f"{API_PREFIX}/posts/{post_id}/pin"
