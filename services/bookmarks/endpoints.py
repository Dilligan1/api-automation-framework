# Эндпоинты закладок.

from config.stages import API_PREFIX


class BookmarkEndpoints:
    bookmarks = f"{API_PREFIX}/bookmarks"

    @staticmethod
    def of_post(post_id: str) -> str:
        return f"{API_PREFIX}/posts/{post_id}/bookmark"
