from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify, url_for, flash
from flask_login import current_user, login_user, logout_user
import os
from sqlalchemy import and_
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Student, Task, login_manager
from datetime import datetime
from io import BytesIO
from fileinput import filename
from hashlib import sha256
from create_app import app
from create_db import create_database_if_not_exists


@login_manager.user_loader
def load_user(user_id):
    db = SessionLocal()
    u = db.get(Student, int(user_id))
    # u = db.query(Student).filter(Student.email == user_email).first()
    db.close()
    return u


create_database_if_not_exists()

old_render_template = render_template

def new_render_template(*args, **kwargs):
    return old_render_template(*args, **kwargs, current_user=current_user)

render_template = new_render_template
# сделал подставление current_user в render templates

def add_task(source: str, statement: str,  number: int, difficulty: int, answer: int, file_name: str, solution: str = "NO"):
    db = SessionLocal()
    try:
        new_task = Task(
            source = source,
            statement=statement, 
            number=number, 
            answer = answer,
            solution = solution,
            difficulty=difficulty,
            file_name = file_name
            )
        db.add(new_task)
        db.commit()
    finally:
        db.close()


def add_student(name: str,  surname: str, patronymic: str, class_number: int, email: str, login: str, password: str, avatar: str):
    db = SessionLocal()
    try:
        new_student = Student()
        new_student.name = name
        new_student.surname = surname
        new_student.patronymic = patronymic
        new_student.class_number = class_number 
        new_student.email = email
        new_student.login = login
        new_student.password = password
        new_student.avatar = avatar
        db.add(new_student)
        db.commit()
    finally:
        db.close()

def authorize(email: str, password: str):
    db = SessionLocal()
    q = db.query(Student).filter(Student.email == email).first()
    if q:
        if q.password == password:
            return True
    return False


def get_tasks(number_array, difficulty):
    db = SessionLocal()
    try:
        return db.query(Task).filter(and_(Task.number.in_(number_array), Task.difficulty.in_(difficulty))).order_by(Task.number).all()
    finally:
        db.close()

@app.route("/add_task_form", methods=['GET', 'POST'])
def add_task_form():
    if request.method == "POST":
        source = request.form["source"]
        statement = request.form["statement"]
        number = int(request.form["number"])
        difficulty = int(request.form.get("select_difficulty"))
        answer = int(request.form["answer"])
        solution = request.form["solution"]
        f = request.files['file']
        filename = f.filename
        if len(filename) != 0:
            f.save(f"static/img/{filename}")
        add_task(source, statement, number, difficulty, answer, filename, solution)
        return render_template("success_add.html")
    return render_template("add_task_form.html")

def get_user_by_email(email):
    db = SessionLocal()
    q = db.query(Student).filter(Student.email == email).first()
    return q
    

def get_student_by_id(id):
    db = SessionLocal()
    q = db.query(Student).get(id)
    return q

@app.route('/')
def main_page():
    return render_template("main_page.html")

@app.route("/tasks", methods=['GET', 'POST'])    
def tasks():
    number_array = list(range(1, 28))
    difficulty = list(range(0, 3))
    checkbox_task_checked = [True] * 28
    checkbox_difficulty_checked = [True] * 3
    if request.method == "POST":
        number_array.clear()
        difficulty.clear()
        for i in range(1, 28):  
            if f"checkbox_task_{i}" in request.form:
                number_array.append(i)
            else:
                checkbox_task_checked[i] = False
        for i in range(3):
            if f"difficulty_{i}" in request.form:
                difficulty.append(i)
            else:
                 checkbox_difficulty_checked[i] = False
    tasks = get_tasks(number_array, difficulty)
    return render_template("tasks.html", tasks = tasks, checkbox_task_checked = checkbox_task_checked, checkbox_difficulty_checked = checkbox_difficulty_checked)


@app.route("/register_choice", methods=['GET', 'POST'])
def register_choice():
    if request.method == "POST":
        return redirect(url_for("home"))
    return render_template("register_choice.html")


@app.route("/register_teacher", methods=['GET', 'POST'])
def register_teacher():
    if request.method == "POST":
        return redirect(url_for("main_page"))
    return render_template("register_teacher.html")


@app.route("/register_student", methods=['GET', 'POST'])
def register_student():
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        patronymic = request.form["patronymic"]
        class_number = int(request.form["num_class"])
        email = request.form["email"]
        login = request.form["login"]
        password = request.form["password"]
        avatar = request.files["avatar"]
        filename = avatar.filename
        if len(filename) != 0:
            avatar.save(f"static/img/avatars/{filename}")
        else:
            filename = "base_avatar.png"
        add_student(name, surname, patronymic, class_number, email, login, password, filename)
        return redirect(url_for("main_page"))
    return render_template("register_student.html")

@app.route("/login_form", methods=['GET', 'POST'])
def login_form():
    msg = ""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if authorize(email, password):
            q = get_user_by_email(email)
            print("login", login_user(q))
            return redirect(url_for("profile"))
        return render_template("login_form.html", msg="Неправильный логин или пароль")
    return render_template("login_form.html", msg=msg)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main_page"))

@app.route("/profile/<id>", methods=['GET', 'POST'])
@app.route("/profile", methods=['GET', 'POST'])
def profile(id=None):
    if id is None:
        user = current_user
    else:
        user = get_student_by_id(id)
    return render_template("profile.html", user=user)


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=8080, host="127.0.0.2", debug=True)   