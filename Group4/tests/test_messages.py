class TestCreateMessage:
    def test_create_message_by_chat_member(self, messages_client):
        payload = {"text": "Привет всем from Postman!", "author_id": 4, "chat_id": 3}
        response = messages_client.create_message(payload)

        assert response.status_code == 200
        data = response.json()
        assert data["text"] == "Привет всем from Postman!"
        assert data["author_id"] == 4
        assert data["chat_id"] == 3
        assert "id" in data
        assert "created_at" in data

    def test_create_message_by_non_member(self, messages_client):
        payload = {"text": "Привет всем from Postman!", "author_id": 2, "chat_id": 3}
        response = messages_client.create_message(payload)

        assert response.status_code == 403
        assert response.json()["detail"] == "User is not a member of this chat"

    def test_create_message_nonexistent_author(self, messages_client):
        payload = {"text": "Привет всем from Postman!", "author_id": 999, "chat_id": 3}
        response = messages_client.create_message(payload)

        assert response.status_code == 404
        assert response.json()["detail"] == "Author not found"

    def test_create_message_nonexistent_chat(self, messages_client):
        payload = {"text": "Привет всем from Postman!", "author_id": 1, "chat_id": 999}
        response = messages_client.create_message(payload)

        assert response.status_code == 404
        assert response.json()["detail"] == "Chat not found"

    def test_create_message_text_is_number(self, messages_client):
        payload = {"text": 123, "author_id": 1, "chat_id": 1}
        response = messages_client.create_message(payload)

        assert response.status_code == 422
        error = response.json()["detail"][0]
        assert error["type"] == "string_type"
        assert error["loc"] == ["body", "text"]

    def test_create_message_author_id_is_string(self, messages_client):
        payload = {"text": "Postman Test", "author_id": "test", "chat_id": 1}
        response = messages_client.create_message(payload)

        assert response.status_code == 422
        error = response.json()["detail"][0]
        assert error["type"] == "int_parsing"
        assert error["loc"] == ["body", "author_id"]

    def test_create_message_chat_id_is_string(self, messages_client):
        payload = {"text": "Postman Test", "author_id": 1, "chat_id": "test"}
        response = messages_client.create_message(payload)

        assert response.status_code == 422
        error = response.json()["detail"][0]
        assert error["type"] == "int_parsing"
        assert error["loc"] == ["body", "chat_id"]

    def test_create_message_empty_text(self, messages_client):
        payload = {"text": "", "author_id": 1, "chat_id": 1}
        response = messages_client.create_message(payload)

        assert response.status_code == 422


class TestGetMessages:
    def test_get_all_messages(self, messages_client):
        response = messages_client.get_messages()

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        for message in data:
            assert "id" in message
            assert "text" in message
            assert "author_id" in message
            assert "chat_id" in message
            assert "created_at" in message

    def test_get_message_by_existing_id(self, messages_client):
        response = messages_client.get_message(2)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 2
        assert "text" in data
        assert "author_id" in data
        assert "chat_id" in data
        assert "created_at" in data

    def test_get_message_by_nonexistent_id(self, messages_client):
        response = messages_client.get_message(999)

        assert response.status_code == 404
        assert response.json()["detail"] == "Message not found"


class TestGetChatMessages:
    def test_get_chat_messages_existing_chat(self, chats_client):
        response = chats_client.get_chat_messages(2)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        for message in data:
            assert message["chat_id"] == 2
            assert "id" in message
            assert "text" in message
            assert "author_id" in message
            assert "created_at" in message

    def test_get_chat_messages_nonexistent_chat(self, chats_client):
        response = chats_client.get_chat_messages(999)

        assert response.status_code == 404
        assert response.json()["detail"] == "Chat not found"
