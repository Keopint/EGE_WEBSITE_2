from database import engine, SessionLocal
from load_tasks import add_tasks
from models import Base, Student, Teacher
from os.path import exists

def add_start_student():
    db = SessionLocal()
    new_student = Student(name="Alice", surname="Aboba", patronymic = "SUS", class_number=10, password=123, login="KOTYA", email="a@gmail.com", avatar="base_avatar.png")
    db.add(new_student)
    db.commit()
    db.close()

def create_database_if_not_exists():
    if not exists("Ege.db"):
        Base.metadata.create_all(bind=engine)
        add_tasks()
        add_start_student()

def main():
    create_database_if_not_exists()
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