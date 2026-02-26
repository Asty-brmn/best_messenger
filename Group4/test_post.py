import requests

# URL вашего API
url = "http://127.0.0.1:8000/messages"

# Данные для отправки
data = {
    "name": "Тестовое сообщение",
    "description": "Это описание сообщения"
}

# Отправка POST запроса
response = requests.post(url, json=data)

# Вывод результата
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")

