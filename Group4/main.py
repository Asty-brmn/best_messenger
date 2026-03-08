from fastapi import FastAPI
from routers import messages, chats, users

from database import init_db

app = FastAPI()


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/")
def root():
    return {"message": "Yra, pobeda!"}


app.include_router(messages.router)
app.include_router(chats.router)
app.include_router(users.router)
