# api/chats_client.py
from api.base_client import BaseClient


class ChatsClient(BaseClient):
    def get_chats(self):
        return self.session.get(f"{self.base_url}/chats")

    def get_chat(self, chat_id: int):
        return self.session.get(f"{self.base_url}/chats/{chat_id}")

    def create_chat(self, payload: dict):
        return self.session.post(f"{self.base_url}/chats", json=payload)

    def get_chat_messages(self, chat_id: int):
        return self.session.get(f"{self.base_url}/chats/{chat_id}/messages")