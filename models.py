from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base
from flask_login import UserMixin, LoginManager
from create_app import login_manager

class Class(Base):
    __tablename__ = 'Class'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    teacher_id = Column(Integer, nullable=False)
    count_student = Column(Integer, nullable=False)


class Teacher(Base):
    __tablename__ = 'Teacher'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    patronymic = Column(Text, nullable=False)
    year = Column(Integer, nullable=False)

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return "TeacherId" + str(self.id)


class class_test(Base):
    __tablename__ = 'class_test'

    id = Column(Integer, primary_key=True, autoincrement=True)
    class_id = Column(Integer, nullable=False)
    test_id = Column(Integer, nullable=False)


class Student(UserMixin, Base):
    __tablename__ = 'Student'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    patronymic = Column(Text, nullable=False)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    class_number = Column(Integer, nullable=False)
    avatar = Column(String, nullable=False)

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)


class class_student(Base):
    __tablename__ = 'class_student'

    id = Column(Integer, primary_key=True, autoincrement=True)
    class_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)

class Test(Base):
    __tablename__ = 'Test'

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, nullable=False)
    attemps_count = Column(Integer, nullable=False)
    task_count = Column(Integer, nullable=False)

class Task(Base):
    __tablename__ = 'Task'

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(Text, nullable=False)
    statement = Column(Text, nullable=False)
    number = Column(Integer, nullable=False)
    answer = Column(Integer, nullable=False)
    solution = Column(Text, nullable=False)
    difficulty = Column(Integer, nullable=False)
    file_name = Column(String, )

class test_task(Base):
    __tablename__ = 'test_task'

    id = Column(Integer, primary_key=True, autoincrement=True)
    test_id = Column(Integer, nullable=False)
    task_id = Column(Integer, nullable=False)