"""
Скрипт для инициализации базы данных
Запуск: python init_db.py
"""
from database import SessionLocal, User, Chat, Message

def create_sample_data():
    """Создает тестовые данные для демонстрации"""
    db = SessionLocal()
    user1 = User(username="alice")
    user2 = User(username="bob")
    user3 = User(username="charlie")
        
    db.add_all([user1, user2, user3])
    db.commit()
    
    chat1 = Chat(name="General Chat")
    chat1.users = [user1, user2, user3]
    
    db.add(chat1)
    db.commit()
    
    message1 = Message(text="Привет всем!", author_id=user1.id, chat_id=chat1.id)
    message2 = Message(text="Как дела?", author_id=user2.id, chat_id=chat1.id)
    message3 = Message(text="Всё отлично!", author_id=user3.id, chat_id=chat1.id)
    
    db.add_all([message1, message2, message3])
    db.commit()


if __name__ == "__main__":
    create_sample_data()

