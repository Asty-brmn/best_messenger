# api/base_client.py
import requests
from dotenv import load_dotenv
import os

load_dotenv()

class BaseClient:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})