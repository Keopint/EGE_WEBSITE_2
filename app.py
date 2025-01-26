from flask import (Flask, render_template, request, redirect,
                   url_for, send_file, jsonify, url_for, flash,
                   render_template_string)
from flask_login import current_user, login_user, logout_user
import os
from sqlalchemy import and_, select, asc, desc
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Student, Task, Post, login_manager
from datetime import datetime
from io import BytesIO
from fileinput import filename
from hashlib import sha256
from create_app import app
from create_db import create_database_if_not_exists
from random import choices
from string import ascii_letters
from md_to_html import markdown_to_html
from bs4 import BeautifulSoup


@login_manager.user_loader
def load_user(user_id):
    db = SessionLocal()
    u = db.get(Student, int(user_id))
    # u = db.query(Student).filter(Student.email == user_email).first()
    db.close()
    return u

create_database_if_not_exists()

def add_render_arguments_decorator(func):
    def new_func(*args, **kwargs):
        return func(*args, **kwargs, current_user=current_user)
    return new_func

render_template = add_render_arguments_decorator(render_template)
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

def renamed_file(filename):
    expansion = filename[filename.rfind("."):]
    newname = "".join(choices(ascii_letters, k=12))
    return newname + expansion

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

def get_user_by_email(email):
    db = SessionLocal()
    q = db.query(Student).filter(Student.email == email).first()
    return q
    

def get_student_by_id(id):
    db = SessionLocal()
    q = db.query(Student).get(id)
    return q

def add_post_to_table(name: str,  text: str, avatar_name: str, video_link: str):
    db = SessionLocal()
    try:
        new_post = Post(
            name=name, 
            text=text, 
            avatar_name=avatar_name,
            video_link = video_link
            )
        db.add(new_post)
        db.commit()
    finally:
        db.close()

def get_post_by_id(id):
    db = SessionLocal()
    try:
        q = db.query(Post).get(id)
    finally:
        db.close()
    return q

def get_name_by_id(id):
    db = SessionLocal()
    try:
        table = db.query(Post).get(id)
        name = table.name
    finally:
        db.close()
    return name

def change_post(id: int, name: str,  text: str, avatar_name: str, video_link: str):
    db = SessionLocal()
    post = db.query(Post).get(id)
    try:
        post.name = name
        post.text = text
        if avatar_name != "book.jpg":
            post.avatar_name = avatar_name
        post.video_link = video_link
        db.commit()
    finally:
        db.close()

def delete_post(id):
    db = SessionLocal()
    post = db.query(Post).get(id)
    if post:
        try:
            file_path = f"static/img/posts_img/{post.avatar_name}"
            if os.path.exists(file_path):
                os.remove(file_path) 
            db.delete(post)
            db.commit()
        finally:
            db.close()

def get_posts():
    db = SessionLocal()
    try:
        posts = db.query(Post).order_by(desc(Post.id)).all()
    finally:
        db.close()
    if len(posts) == 0:
        return []
    return posts

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
        filename = renamed_file(f.filename)
        if len(filename) != 0:
            f.save(f"static/img/{filename}")
        add_task(source, statement, number, difficulty, answer, filename, solution)
        return render_template("success_task_add.html")
    return render_template("add_task_form.html")

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
        filename = renamed_file(avatar.filename)
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
        user: Student = get_student_by_id(id)
    return render_template("profile.html", user=user)

@app.route("/add_post", methods=['POST', 'GET'])
def add_post():
    if request.method == "POST":
        if "send_post" in request.form:
            name = request.form['name']
            text = request.form['text']
            image = request.files['file']
            avatar_name = renamed_file(image.filename)
            video_link = request.form["video_link"]
            if len(image.filename) != 0:
                image.save(f"static/img/posts_img/{avatar_name}")
            else:
                avatar_name = "book.jpg"

            add_post_to_table(name, text, avatar_name, video_link)
            return render_template("success_post_add.html", name=name)
            
    return render_template("add_post.html")

@app.route("/posts/<int:id>/delete")
def post_delete(id):
    name = get_name_by_id(id)
    delete_post(id)
    return render_template("success_post_delete.html", name=name)

@app.route("/posts/<int:id>/update", methods=['GET', 'POST'])
def post_update(id):
    table: Post = get_post_by_id(id)
    is_generate = False
    answer_dialog = ""
    if request.method == "POST":
        if "send_post" in request.form:
            name = request.form['name']
            text = request.form['text']
            image = request.files['file']
            avatar_name = renamed_file(image.filename)
            video_link = request.form["video_link"]
            if len(image.filename) != 0:
                image.save(f"static/img/posts_img/{avatar_name}")
            else:
                avatar_name = "book.jpg"
            try:
                change_post(id, name, text, avatar_name, video_link)
                return render_template("success_post_update.html", name=table.name)
            except:
                return "ОШИБКА ВЫПОЛНЕНИЯ ПРОГРАММЫ"
    return render_template("post_update.html", table=table, cnt_row=str(table.text).count('\n') + 1)

@app.route("/posts")
def posts():
    tables = get_posts()
    return render_template("posts.html", tables=tables)

@app.route("/posts/<int:id>")
def post_detail(id):
    table: Post = get_post_by_id(id)
    return render_template("post.html", table=table, cnt_row=str(table.text).count('\n') + 1)

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=8080, host="127.0.0.2", debug=True)