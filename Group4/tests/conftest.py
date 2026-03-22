# tests/conftest.py
import pytest
from api.messages_client import MessagesClient
from api.chats_client import ChatsClient


@pytest.fixture(scope="session")
def messages_client():
    return MessagesClient()


@pytest.fixture(scope="session")
def chats_client():
    return ChatsClient()
