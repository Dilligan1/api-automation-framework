# Эндпоинты личных и групповых диалогов.

from config.stages import API_PREFIX


class MessageEndpoints:
    conversations = f"{API_PREFIX}/conversations"

    @staticmethod
    def dm(username: str) -> str:
        """Найти существующий 1:1 диалог или создать новый."""
        return f"{API_PREFIX}/conversations/dm/{username}"

    @staticmethod
    def by_id(conversation_id: str) -> str:
        return f"{API_PREFIX}/conversations/{conversation_id}"

    @staticmethod
    def messages(conversation_id: str) -> str:
        return f"{API_PREFIX}/conversations/{conversation_id}/messages"

    @staticmethod
    def read(conversation_id: str) -> str:
        return f"{API_PREFIX}/conversations/{conversation_id}/read"

    @staticmethod
    def message(message_id: str) -> str:
        return f"{API_PREFIX}/messages/{message_id}"
