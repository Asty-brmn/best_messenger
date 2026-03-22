

class TestCreateChat:
    def test_create_chat_with_existing_users(self, chats_client):
        payload = {"name": "Postman chat", "user_ids": [1, 3, 4]}
        response = chats_client.create_chat(payload)

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Postman chat"
        assert "id" in data
        user_ids = [user["id"] for user in data["users"]]
        assert set(user_ids) == {1, 3, 4}

    def test_create_chat_with_nonexistent_users(self, chats_client):
        payload = {"name": "Secret", "user_ids": [1, 999]}
        response = chats_client.create_chat(payload)

        assert response.status_code == 404
        assert response.json()["detail"] == "Some users not found"

    def test_create_chat_name_is_number(self, chats_client):
        payload = {"name": 123, "user_ids": [1, 999]}
        response = chats_client.create_chat(payload)

        assert response.status_code == 422
        error = response.json()["detail"][0]
        assert error["type"] == "string_type"
        assert error["loc"] == ["body", "name"]

    def test_create_chat_user_ids_is_string(self, chats_client):
        payload = {"name": "t", "user_ids": "test"}
        response = chats_client.create_chat(payload)

        assert response.status_code == 422
        error = response.json()["detail"][0]
        assert error["type"] == "list_type"
        assert error["loc"] == ["body", "user_ids"]

    def test_create_chat_user_ids_contains_invalid_type(self, chats_client):
        payload = {"name": "t", "user_ids": [1, "abc"]}
        response = chats_client.create_chat(payload)

        assert response.status_code == 422
        error = response.json()["detail"][0]
        assert error["type"] == "int_parsing"
        assert error["loc"] == ["body", "user_ids", 1]


class TestGetChats:
    def test_get_all_chats(self, chats_client):
        response = chats_client.get_chats()

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        for chat in data:
            assert "id" in chat
            assert "name" in chat
            assert "users" in chat

    def test_get_chat_by_existing_id(self, chats_client):
        response = chats_client.get_chat(2)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 2
        assert "name" in data
        assert "users" in data

    def test_get_chat_by_nonexistent_id(self, chats_client):
        response = chats_client.get_chat(999)

        assert response.status_code == 404
        assert response.json()["detail"] == "Chat not found"
