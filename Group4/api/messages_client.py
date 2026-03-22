# api/messages_client.py
from api.base_client import BaseClient


class MessagesClient(BaseClient):
    def get_messages(self):
        return self.session.get(f"{self.base_url}/messages")

    def get_message(self, message_id: int):
        return self.session.get(f"{self.base_url}/messages/{message_id}")

    def create_message(self, payload: dict):
        return self.session.post(f"{self.base_url}/messages", json=payload)
