"""
Скрипт для инициализации базы данных
Запуск: python init_db.py
"""

from database import SessionLocal, User, Chat, Message


def create_sample_data():
    """Создает тестовые данные для демонстрации"""
    db = SessionLocal()

    # Пользователи
    user1 = User(username="alice")
    user2 = User(username="bob")
    user3 = User(username="charlie")

    db.add_all([user1, user2, user3])
    db.commit()

    # Первый чат
    chat1 = Chat(name="General Chat")
    chat1.users = [user1, user2, user3]

    db.add(chat1)
    db.commit()

    message1 = Message(text="Привет всем!", author_id=user1.id, chat_id=chat1.id)
    message2 = Message(text="Как дела?", author_id=user2.id, chat_id=chat1.id)
    message3 = Message(text="Всё отлично!", author_id=user3.id, chat_id=chat1.id)

    db.add_all([message1, message2, message3])
    db.commit()

    # Второй чат
    chat2 = Chat(name="Second Chat")
    chat2.users = [user1, user2]  # приватный чат между alice и bob

    db.add(chat2)
    db.commit()

    message4 = Message(text="Привет, Bob!", author_id=user1.id, chat_id=chat2.id)
    message5 = Message(
        text="Привет, Alice! Что нового?", author_id=user2.id, chat_id=chat2.id
    )

    db.add_all([message4, message5])
    db.commit()

    db.close()


if __name__ == "__main__":
    create_sample_data()
