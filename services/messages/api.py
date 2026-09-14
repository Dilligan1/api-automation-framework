# Сервисный класс диалогов: личные и групповые чаты, отправка и чтение сообщений.

import allure

from services.common.models.responses import PaginatedResponse
from services.messages.endpoints import MessageEndpoints
from services.messages.models.responses import ConversationResponse, MessageResponse
from services.messages.payloads import CreateConversationPayload, SendMessagePayload
from utils.api_helper import APIHelper
from utils.http_client import HTTPClient


class MessageAPI(APIHelper):
    def __init__(self, client: HTTPClient, token: str) -> None:
        self.client = client
        self.token = token
        self.endpoints = MessageEndpoints()

    @allure.step("Список диалогов")
    def list_conversations(self, **kwargs) -> PaginatedResponse[ConversationResponse]:
        response = self.client.get(
            self.endpoints.conversations, headers=self._auth_headers
        )
        return self._validate_response(
            response, PaginatedResponse[ConversationResponse], **kwargs
        )

    @allure.step("Создание группового диалога")
    def create_conversation(
        self, payload: CreateConversationPayload, status_code: int = 201, **kwargs
    ) -> ConversationResponse:
        response = self.client.post(
            self.endpoints.conversations,
            json=payload.model_dump(exclude_none=True),
            headers=self._auth_headers,
        )
        return self._validate_response(response, ConversationResponse, status_code, **kwargs)

    @allure.step("Поиск или создание 1:1 диалога с @{username}")
    def find_or_create_dm(self, username: str, **kwargs) -> ConversationResponse:
        response = self.client.post(
            self.endpoints.dm(username), headers=self._auth_headers
        )
        return self._validate_response(response, ConversationResponse, **kwargs)

    @allure.step("Карточка диалога {conversation_id}")
    def get_conversation(self, conversation_id: str, **kwargs) -> ConversationResponse:
        response = self.client.get(
            self.endpoints.by_id(conversation_id), headers=self._auth_headers
        )
        return self._validate_response(response, ConversationResponse, **kwargs)

    @allure.step("Сообщения диалога {conversation_id}")
    def list_messages(
        self, conversation_id: str, **kwargs
    ) -> PaginatedResponse[MessageResponse]:
        response = self.client.get(
            self.endpoints.messages(conversation_id), headers=self._auth_headers
        )
        return self._validate_response(
            response, PaginatedResponse[MessageResponse], **kwargs
        )

    @allure.step("Отправка сообщения в диалог {conversation_id}")
    def send_message(
        self, conversation_id: str, payload: SendMessagePayload, status_code: int = 201, **kwargs
    ) -> MessageResponse:
        response = self.client.post(
            self.endpoints.messages(conversation_id),
            json=payload.model_dump(),
            headers=self._auth_headers,
        )
        return self._validate_response(response, MessageResponse, status_code, **kwargs)

    @allure.step("Удаление сообщения {message_id}")
    def delete_message(self, message_id: str, status_code: int = 204, **kwargs) -> None:
        response = self.client.delete(
            self.endpoints.message(message_id), headers=self._auth_headers
        )
        return self._validate_response(response, None, status_code, **kwargs)

    @allure.step("Отметить диалог {conversation_id} прочитанным")
    def mark_read(self, conversation_id: str, status_code: int = 204, **kwargs) -> None:
        response = self.client.post(
            self.endpoints.read(conversation_id), headers=self._auth_headers
        )
        return self._validate_response(response, None, status_code, **kwargs)
