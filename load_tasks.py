from sqlalchemy.orm import Session
from database import SessionLocal
from models import Student, Task
import random

def add_task(statement: str,  number: int, difficulty: int, answer: int, solution: str = "NO"):
    db = SessionLocal()
    try:
        new_task = Task(
                statement=statement, 
                number=number, 
                answer = answer,
                solution = solution,
                difficulty=difficulty
            )
        db.add(new_task)
        db.commit()
    finally:
        db.close()


def get_tasks():
    db = SessionLocal()
    try:
        return db.query(Task).all()
    finally:
        db.close()

def add_tasks():
    db = SessionLocal()
    try:
        with open("static/img/tasks.txt", encoding="utf-8") as f:
            tasks = []
            t = {}
            for line in f.readlines():
                if not line.strip():
                    continue
                line = line.strip()
                if line[0] == "#":
                    if t:   
                        tasks.append(t)
                    e = line[1:].strip().split()
                    t = {"type": e[0], "ans": e[1], "descr": ""}
                    if len(e) > 2:
                        t["file"] = e[2]
                else:
                    t["descr"] += line + "\n"
            if t:
                tasks.append(t)
            
        for e in tasks:
            new_task = Task()
            new_task.source = "kompege.ru"
            new_task.number = int(e["type"])
            new_task.answer = int(e["ans"])
            new_task.statement = str(e["descr"]).replace('\n', '<br>')
            new_task.difficulty = random.randint(0, 2)
            new_task.solution = "No"
            if "file" in e.keys():
                new_task.file_name = e["file"]
            else:
                new_task.file_name = None
            db.add(new_task)
            db.commit()
                
                
    finally:
        db.close()


def main():
    add_tasks()


if __name__ == '__main__':
    main()