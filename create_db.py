from database import engine, SessionLocal
from models import Base, Student

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Пример использования сессии
def main():
    # Создание новой сессии
    db = SessionLocal()
    try:
        # Пример добавления нового пользователя
        new_student = Student(name="Alice", surname="Aboba", patronymic = "SUS", class_number=10, password=123, login="KOTYA", email="aboba@mail.ru", avatar="base_avatar.png")
        db.add(new_student)
        db.commit()
    finally:
        db.close()

if __name__ == '__main__':
    main()