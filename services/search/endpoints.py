# Эндпоинты поиска и трендов.

from config.stages import API_PREFIX


class SearchEndpoints:
    users             = f"{API_PREFIX}/search/users"
    posts             = f"{API_PREFIX}/search/posts"
    hashtags          = f"{API_PREFIX}/search/hashtags"
    trending_hashtags = f"{API_PREFIX}/search/trending/hashtags"
