from flask import (Flask, render_template, request, redirect,
                   url_for, send_file, jsonify, url_for, flash,
                   render_template_string)
from flask_login import current_user, login_user, logout_user
import os
from sqlalchemy import and_, select, asc, desc
from sqlalchemy.orm import Session, joinedload
from database import SessionLocal
from models import Student, Task, login_manager, Post, Submit, Message, Pitch, PitchImg, Tag, TaskTag
from datetime import datetime
from io import BytesIO
from fileinput import filename
from hashlib import sha256
from create_app import app
from create_db import create_database_if_not_exists
from statistics import get_tasks_per_days, get_data_each_task_type
import json
from random import choices
from string import ascii_letters
from md_to_html import markdown_to_html
from pdf2image import convert_from_path


if not os.path.exists("./presentations"):
    os.makedirs("./presentations")


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

def add_task(source: str, statement: str,  number: int, difficulty: int, answer: int, file_name: str, tags, solution: str = "NO"):
    db = SessionLocal()
    try:
        new_task = Task(
            source=source,
            statement=statement, 
            number=number, 
            answer=answer,
            solution=solution,
            difficulty=difficulty,
            file_name=file_name,
            author=current_user.id
            )
        db.add(new_task)
        db.commit()
        for tag_name in tags:
            tag_name = tag_name.strip().lower()  # Удаляем пробелы
            if tag_name:  # Проверяем, что тег не пустой
                tag = db.query(Tag).filter_by(name=tag_name).first()
                if not tag: 
                    tag = Tag(name=tag_name)
                    db.add(tag)
                    db.commit()  # Сохраняем тег в БД
                
                # Создание связи между заданием и тегом
                task_tag = TaskTag(task_id=new_task.id, tag_id=tag.id)
                db.add(task_tag)
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

def is_subarray(arr1, arr2):  # Создаём копию, чтобы не изменять исходный массив
    for elem in arr1:
        if elem not in arr2:
            return False # Удаляем найденный элемент
    return True

def get_tasks(number_array, difficulty, tags):
    db = SessionLocal()
    print(number_array, difficulty, tags)
    try:
        tasks = []
        if len(tags) > 0:
            without_tags_tasks = db.query(Task).filter(and_(Task.number.in_(number_array), Task.difficulty.in_(difficulty))).order_by(Task.number).options(joinedload(Task.student)).all()
            for t in without_tags_tasks:
                if is_subarray(tags, [tag.name for tag in t.tags]):
                    tasks.append(t)
        else:
            tasks = db.query(Task).filter(and_(Task.number.in_(number_array), Task.difficulty.in_(difficulty))).order_by(Task.number).options(joinedload(Task.student)).all()
    finally:
        db.close()
    return tasks

def get_tags(number_array, difficulty, tags):
    db = SessionLocal()
    tags_for_tasks = []
    try:
        tasks = []
        if len(tags) > 0:
            without_tags_tasks = db.query(Task).filter(and_(Task.number.in_(number_array), Task.difficulty.in_(difficulty))).order_by(Task.number).options(joinedload(Task.student)).all()
            for t in without_tags_tasks:
                if is_subarray(tags, [tag.name for tag in t.tags]):
                    tasks.append(t)
        else:
             tasks = db.query(Task).filter(and_(Task.number.in_(number_array), Task.difficulty.in_(difficulty))).order_by(Task.number).options(joinedload(Task.student)).all()
        for task in tasks:
            tags_for_tasks.append([tag.name for tag in task.tags])
    finally:
        db.close()
    return tags_for_tasks

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
            video_link = video_link,
            author=current_user.id
            )
        db.add(new_post)
        db.commit()
    finally:
        db.close()

def get_post_by_id(id):
    db = SessionLocal()
    try:
        # Используем joinedload для подгрузки связанного студента (автора)
        post = db.query(Post)\
                .options(joinedload(Post.student))\
                .filter(Post.id == id)\
                .first()
    finally:
        db.close()
    return post

def get_task_by_id(id):
    db = SessionLocal()
    try:
        # Используем joinedload для подгрузки связанного студента (автора)
        task = db.query(Task)\
                .options(joinedload(Task.student))\
                .options(joinedload(Task.tags))\
                .filter(Task.id == id)\
                .first()
    finally:
        db.close()
    return task

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
            if post.avatar_name != "book.jpg":
                file_path = f"static/img/posts_img/{post.avatar_name}"
                if os.path.exists(file_path):
                    os.remove(file_path) 
            messages = db.query(Message).filter(Message.post_id == post.id).order_by(Message.date).all()
            for mes in messages:
                db.delete(mes)
            db.delete(post)
            db.commit()
        finally:
            db.close()

def get_posts():
    db = SessionLocal()
    try:
        posts = db.query(Post).options(joinedload(Post.student)) \
                             .order_by(desc(Post.id)) \
                             .all()
        return posts
    finally:
        db.close()

def get_pitches():
    db = SessionLocal()
    try:
        posts = db.query(Pitch).order_by(desc(Pitch.id)).all()
    finally:
        db.close()
    if len(posts) == 0:
        return []
    return posts

def get_pitches():
    db = SessionLocal()
    try:
        posts = db.query(Pitch).order_by(desc(Pitch.id)).all()
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
    difficulty_names = ["Легкая", "Нормальная", "Сложная"]
    difficulty = list(range(0, 3))
    checkbox_task_checked = [True] * 28
    checkbox_difficulty_checked = [True] * 3
    tags = []
    if request.method == "POST":
        number_array.clear()
        difficulty.clear()
        tags = request.form["tags"].split(',')
        if tags[0] == '':
            tags.clear()
        for i in range(len(tags)):
            tags[i] = tags[i].strip().lower()
        print(tags)
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

    tasks_without_tags = get_tasks(number_array, difficulty, tags)
    tags_for_tasks = get_tags(number_array, difficulty, tags)

    tasks = []

    for t in tasks_without_tags:
        print(t.id)

    for i in range(len(tasks_without_tags)):
        tasks.append([tasks_without_tags[i], tags_for_tasks[i]])


    return render_template("tasks.html", tasks = tasks, 
                           checkbox_task_checked = checkbox_task_checked, 
                           checkbox_difficulty_checked = checkbox_difficulty_checked,
                           difficulty_names = difficulty_names)

@app.route("/add_task_form", methods=['GET', 'POST'])
def add_task_form():
    if request.method == "POST":
        source = request.form["source"]
        statement = str(request.form["statement"]).replace('\n', '<br>')
        number = int(request.form["number"])
        difficulty = int(request.form.get("select_difficulty"))
        answer = int(request.form["answer"])
        solution = request.form["solution"]
        f = request.files['file']
        filename = renamed_file(f.filename)
        if len(filename) != 0:
            f.save(f"static/img/{filename}")
            
        tags = request.form.get('tags').split(',') 
        add_task(source, statement, number, difficulty, answer, filename, tags, solution)
        return render_template("success_task_add.html")
    if current_user.is_anonymous:
        return redirect(url_for('login_form'))
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
        user = get_student_by_id(id)
    data_per_day = get_tasks_per_days(user.id)
    data_per_type = get_data_each_task_type(user.id)
    data_per_day_str = [[date.isoformat(), value] for date, value in data_per_day]
    data_per_day_json = json.dumps(data_per_day_str)
    return render_template("profile.html", user=user, data_per_day_json=data_per_day_json, data_per_type=data_per_type)


@app.route("/check_answer", methods=['POST'])
def check_answer():
    data = request.json
    task_id = data.get('task_id')
    user_response = int(data.get('user_response'))
    task_answer = data.get('task_answer')

    try:
        add_submit(task_id, current_user.id, user_response)
    finally:
        return jsonify({"status": "success", "message": "Answer received"})


def add_submit(task_id: int, user_id: int, user_response: int) -> None:
    db = SessionLocal()
    try:
        new_submit = Submit(task_id=task_id, user_id=user_id,
                            user_response=user_response, date=datetime.today())
        db.add(new_submit)
        db.commit()
    finally:
        db.close()

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
    if current_user.is_anonymous:
        return redirect(url_for('login_form'))
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

@app.route("/pitches")
def pitches():
    tables = get_pitches()
    return render_template("pitches.html", tables=tables)

@app.route("/posts/<int:id>")
def post_detail(id):
    table: Post = get_post_by_id(id)
    table_text = markdown_to_html(table.text)
    is_author = False
    if (not current_user.is_anonymous) and current_user.id == table.author:
        is_author = True
    print(table.student)
    return render_template("post.html", table=table, cnt_row=str(table.text).count('\n') + 1, forum=get_forum(SessionLocal(), table), table_text=table_text, is_author=is_author)

def get_forum(db: Session, post: Post):
    mes = reversed(db.query(Message).filter(Message.post_id == post.id).order_by(Message.date).all())
    with open("templates/forum.html", encoding='utf-8') as f:
        template = f.read()
    return render_template_string(template, messages=mes)

@app.route("/api/forum/<int:post_id>", methods=['GET', 'POST'])
def api_forum(post_id):
    db = SessionLocal()
    post: Post = db.query(Post).get(int(post_id))
    if request.method == "POST":
        data = request.json
        text = data.get('text')
        mes = Message(post_id=post.id, user_id=current_user.id, text=text)
        db.add(mes)
        db.commit()
    # content-type json

    print("FORUM")
    print(get_forum(db, post))
    return jsonify({"data": get_forum(db, post)})

@app.route("/pitch/<int:id>")
def watch_pitch(id):
    with SessionLocal() as db:
        pitch = db.query(Pitch).filter(Pitch.id==id).first()
        images = db.query(PitchImg).filter(PitchImg.pitch_id==id).order_by(PitchImg.id).all()
    return render_template("pitch.html", pitch=pitch, images=images)

@app.route("/add_pitch", methods=["GET", "POST"])
def add_pitch():
    if request.method == "POST":
        with SessionLocal() as db:
            avatar_name = renamed_file(request.files["img"].filename)
            if not request.files["img"].filename:
                avatar_name = "base_avatar.png"
            request.files["img"].save("./static/img/posts_img/" + avatar_name)
            pitch = Pitch(
                name=request.form["name"],
                avatar_name=avatar_name)
            db.add(pitch)
            db.commit()
            pdfname = renamed_file(request.files["pdf"].filename)
            request.files["pdf"].save(f"./presentations/" + pdfname)
            images = convert_from_path("./presentations/" + pdfname)
            os.makedirs(f"./static/pitches/{pdfname[:-4]}")
            for i, image in enumerate(images):
                newname = f"./static/pitches/{pdfname[:-4]}/page_{i}.png"
                image.save(newname)
                pitchimg = PitchImg(pitch_id=pitch.id, url="." + newname)
                db.add(pitchimg)
                db.commit()
        return redirect("/")
    if current_user.is_anonymous:
        return redirect(url_for('login_form'))
    return render_template("add_pitch.html")

@app.route('/get_task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = get_task_by_id(task_id)
    difficulty_names = ["Легкая", "Нормальная", "Сложная"]
    tags = ' #'.join(tag.name for tag in task.tags)
    if len(tags) > 0:
        tags = '#' + tags
    if task:
        return jsonify({
            "task_html" : f'''
                <div class="task-item border rounded p-3 mb-3">
                    <!-- Мета-данные задания -->
                    <div class="d-flex flex-wrap gap-3 bg-light border rounded p-3 mb-3">
                        <div class="d-flex align-items-center">
                            <span class="fw-bold text-secondary me-1">Id:</span>
                            <span>{ task.id }</span>
                        </div>
                        <div class="d-flex align-items-center">
                            <span class="fw-bold text-secondary me-1">Источник:</span>
                            <span>{ task.source }</span>
                        </div>
                        <div class="d-flex align-items-center">
                            <span class="fw-bold text-secondary me-1">№ КИМ:</span>
                            <span>{ task.number }</span>
                        </div>
                        <div class="d-flex align-items-center">
                            <span class="fw-bold text-secondary me-1">Сложность:</span>
                            <span>
                                { difficulty_names[task.difficulty]}
                            </span>
                        </div>
                    </div> 
                    <p class="mt-2">{ task.statement}</p>
                    <p>
                        {tags}
                    </p>
                '''
        })
    return jsonify({'error': 'Task not found'}), 404

@app.route("/add_variant", methods=["GET", "POST"])
def add_variant():
    if current_user.is_anonymous:
        return redirect(url_for('login_form'))
    return render_template("add_variant.html")

@app.route("/variants", methods=["GET", "POST"])
def variants():
    if current_user.is_anonymous:
        return redirect(url_for('login_form'))
    return render_template("variants.html")

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=8080, host="127.0.0.2", debug=True)