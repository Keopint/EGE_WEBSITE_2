import inspect
from functools import wraps
from sqlalchemy import and_, delete
from sqlalchemy.orm import Session
from models import Class, Task, Student, class_student
from database import SessionLocal
import uuid


def convert_params(*params):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_args = inspect.signature(func).bind(*args, **kwargs)
            bound_args.apply_defaults()

            updates = {}
            with SessionLocal() as db:
                for param_name, param_class in params:
                    value = bound_args.arguments.get(param_name)
                    if isinstance(value, int):
                        filters = [param_class.id == value]
                        if param_class == Student:
                            role = 'student' if param_name == 'student' else 'teacher' if param_name == 'teacher' else None
                            if role:
                                filters.append(param_class.role == role)

                        obj = db.query(param_class).filter(and_(*filters)).first()
                        if not obj:
                            return

                        updates[param_name] = obj

            bound_args.arguments.update(updates)
            return func(*bound_args.args, **bound_args.kwargs)

        return wrapper

    return decorator


@convert_params(('student', Student), ('_class', Class))
def add_student_to_class(student: Student | int, _class: Class | int) -> None:
    with SessionLocal() as db:
        new_row = class_student(class_id=_class.id, student_id=student.id)
        db.add(new_row)
        _class.count_student += 1
        db.commit()


@convert_params(('student', Student), ('_class', Class))
def remove_student_from_class(student: Student | int, _class: Class | int) -> None:
    with SessionLocal() as db:
        _class_student = db.query(class_student).filter(
            and_(
                class_student.class_id == _class.id,
                class_student.student_id == student.id
            )
        ).first()
        if _class_student:
            _class.count_student -= 1
            db.delete(_class_student)
            db.commit()


@convert_params(('teacher', Student))
def create_class(teacher: Student | int, name: str) -> None:
    with SessionLocal() as db:
        new_class = Class(name=name, teacher_id=teacher.id, code=generate_unique_key())
        db.add(new_class)
        db.commit()


@convert_params(('_class', Class))
def delete_class(_class: Class | int) -> None:
    with SessionLocal() as db:
        db.execute(delete(class_student).where(class_student.class_id == _class.id))
        db.execute(delete(Class).where(Class.id == _class.id))
        db.commit()


@convert_params(('_class', Class))
def get_all_students_of_class(_class: Class | int) -> list:
    with SessionLocal() as db:
        return db.query(class_student).filter(class_student.class_id == _class.id).all()


def get_class_by_code(code: str) -> Class | None:
    with SessionLocal() as db:
        _class = db.query(Class).filter(Class.code == code)
        if len(_class) == 1:
            return _class.first()
        else:
            return None


def generate_unique_key() -> str:
    return str(uuid.uuid4())
