from models import Submit, Task
from database import SessionLocal


def get_all_submits_of_user(user_id: int) -> list:
    db = SessionLocal()
    return db.query(Submit).filter(Submit.user_id == user_id)


def get_tasks_per_days(user_id: int) -> list[list]:
    submits = get_all_submits_of_user(user_id)
    res = {}
    days = set()
    for submit in submits:
        if submit.date not in days:
            days.add(submit.date)
            res[submit.date] = 0
        res[submit.date] += 1

    res = [[date, res[date]] for date in res]
    return res


def get_type_statistics(user_id: int) -> dict:
    submits = get_all_submits_of_user(user_id)
    numbers = {}
    db = SessionLocal()

    for submit in submits:
        task = db.query(Task).filter(Task.id == submit.task_id)[0]
        if task.number not in numbers:
            numbers[task.number] = {'number': 0, 'correct': 0}
        numbers[task.number]['number'] += 1
        numbers[task.number]['correct'] += (1 if submit.user_response == task.answer else 0)

    return numbers


def get_n_sagging_tasks(user_id: int, n: int) -> list[int]:
    numbers = get_type_statistics(user_id)
    numbers = sorted([[number, numbers[number]] for number in numbers],
                     key=lambda x: x[1]['correct'] / x[1]['number'], reverse=True)[:n - 1]
    return [number[0] for number in numbers]


def get_data_each_task_type(user_id: int) -> list[list[str, int, int]]:
    numbers = get_type_statistics(user_id)
    numbers = sorted([[number, numbers[number]['correct'], numbers[number]['number'] - numbers[number]['correct']]
                      for number in numbers], key=lambda x: x[0])
    numbers = list(map(lambda x: ['КИМ ' + str(x[0]), x[1], x[2]], numbers))
    numbers = [['Задание', 'Верно', 'Неправильно']] + numbers
    return numbers


# print(get_tasks_per_days(1))
