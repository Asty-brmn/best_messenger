from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import requests

app = FastAPI()

# Список для хранения сообщений
messages_list: List[dict] = []


class Message(BaseModel):
    name: str
    description: str = None


@app.get("/")
def root():
    return {"message": "Yra, pobeda!"}

@app.post("/messages")
def create_message(message: Message):
    message_dict = message.dict()
    messages_list.append(message_dict)
    return {"message": "Message added", "message": message_dict, "total_messages": len(messages_list)}


@app.get("/messages")
def get_all_messages():
    return {"messages": messages_list, "total": len(messages_list)}


@app.get("/messages/{name}/{description}")
def post_message(name: str, description: str):
    url = "http://127.0.0.1:8000/messages"

    data = {
        "name": name,
        "description": description
    }

    response = requests.post(url, json=data)

    return f"Status Code: {response.status_code}, Response: {response.json()}"