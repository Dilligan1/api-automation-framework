# Сервисный класс поиска и трендов.

import allure

from services.common.models.responses import (
    HashtagResponse,
    PaginatedResponse,
    PostResponse,
    UserBrief,
)
from services.search.endpoints import SearchEndpoints
from utils.api_helper import APIHelper
from utils.http_client import HTTPClient


class SearchAPI(APIHelper):
    def __init__(self, client: HTTPClient, token: str) -> None:
        self.client = client
        self.token = token
        self.endpoints = SearchEndpoints()

    @allure.step("Поиск пользователей по запросу '{query}'")
    def users(self, query: str, **kwargs) -> PaginatedResponse[UserBrief]:
        response = self.client.get(
            self.endpoints.users, params={"q": query}, headers=self._auth_headers
        )
        return self._validate_response(response, PaginatedResponse[UserBrief], **kwargs)

    @allure.step("Поиск постов по запросу '{query}'")
    def posts(self, query: str, **kwargs) -> PaginatedResponse[PostResponse]:
        response = self.client.get(
            self.endpoints.posts, params={"q": query}, headers=self._auth_headers
        )
        return self._validate_response(response, PaginatedResponse[PostResponse], **kwargs)

    @allure.step("Поиск хэштегов по запросу '{query}'")
    def hashtags(self, query: str, **kwargs) -> PaginatedResponse[HashtagResponse]:
        response = self.client.get(
            self.endpoints.hashtags, params={"q": query}, headers=self._auth_headers
        )
        return self._validate_response(
            response, PaginatedResponse[HashtagResponse], **kwargs
        )

    @allure.step("Трендовые хэштеги")
    def trending_hashtags(self, **kwargs) -> list[HashtagResponse]:
        response = self.client.get(
            self.endpoints.trending_hashtags, headers=self._auth_headers
        )
        return self._validate_response(response, HashtagResponse, **kwargs)
