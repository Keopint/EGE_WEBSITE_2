from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from database import Base
from flask_login import UserMixin, LoginManager
from create_app import login_manager

class Class(Base):
    __tablename__ = 'Class'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    teacher_id = Column(Integer, nullable=False)
    count_student = Column(Integer, nullable=False)

class Course(Base):
    __tablename__ = 'Course'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    avatar_name = Column(Text)
    units = relationship("Unit", back_populates="course", cascade="all, delete-orphan")
    date = Column(DateTime, default=lambda: datetime.utcnow().replace(second=0, microsecond=0))


class Unit(Base):
    __tablename__ = 'Unit'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('Course.id', ondelete='CASCADE'), nullable=False)
    name = Column(Text, nullable=False)
    link = Column(Text, nullable=False)
    course = relationship("Course", back_populates="units")


class Post(Base):
    __tablename__ = 'Post'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    text = Column(Text, nullable=False)
    avatar_name = Column(Text)
    video_link = Column(Text)
    date = Column(DateTime, default=lambda: datetime.utcnow().replace(second=0, microsecond=0))

class Pitch(Base):
    __tablename__ = 'Pitch'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    avatar_name = Column(Text)
    date = Column(DateTime, default=lambda: datetime.utcnow().replace(second=0, microsecond=0))
    images = relationship("PitchImg", back_populates="pitch")

class PitchImg(Base):
    __tablename__ = 'PitchImg'

    id = Column(Integer, primary_key=True)
    pitch_id = Column(Integer, ForeignKey("Pitch.id"), nullable=False)
    url = Column(Text, nullable=False)
    pitch = relationship("Pitch", back_populates="images")

class Message(Base):
    __tablename__ = 'Message'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Student.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('Post.id'), nullable=False)
    user = relationship("Student")
    post = relationship("Post")
    text = Column(Text, nullable=False)
    date = Column(DateTime, default=lambda: datetime.now())

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

class Comment(Base):
    __tablename__ = 'Comment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    text = Column(Text, nullable=False)
    data = Column(DateTime, default=datetime.utcnow)


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


class Submit(Base):
    __tablename__ = 'Submit'

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    user_response = Column(Integer)
    date = Column(Date, nullable=False)

