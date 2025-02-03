# Основы веб-разработки и программирования
## Форматирование контента и работа с текстом
### Практические примеры разметки

Рассмотрим базовые элементы HTML. Тег заголовка первого уровня записывается так:  
`<h1> Hello world! </h1>`

В текстовом форматировании используются:
- *Курсив* для выделения терминов
- **Жрный шрифт** для ключевых понятий

---

## Вероятностные модели в компьютерных науках
Важную роль в алгоритмах играет неравенство Хёфдинга:  
$$P(|S - E[S]| \ge t) \le 2 \exp \left( -\frac{2 t^2 n^2}{\sum_{i = 1}^n (b_i - a_i)^2} \right).$$  
Это фундаментальный результат для анализа алгоритмов машинного обучения.

---

## Структурирование информации
При создании технической документации используются:

Нумерованные списки:  
1. Принцип инкапсуляции
2. Иерархия наследования

Маркированные списки:  
* Абстрактные типы данных
* Полиморфные методы

---

## Работа с внешними ресурсами
Пример гиперссылки:  
[Поисковая система Google](https://www.google.com)

Вставка медиа-контента:  
![Пример цифрового архива](https://expositions.nlr.ru/Mayakovsky/images/6_12.jpg)

Вставка видео-контента:
[[https://rutube.ru/video/9e7be120aaac6b1043cc10327d3e0d96/?r=wd]]

> **Цитата дня**: "Программирование — это искусство создавать решения для проблем, которые ещё даже не возникли"

---

## Управление памятью и специальные символы
В языках программирования используются escape-последовательности:  
`\n` - перенос строки  
`\t` - табуляция  
`\s` - пробел

---

## Практикум: Объектно-ориентированное программирование на Python
Рассмотрим пример реализации классов животных с наследованием:

```
import os
import json
import random
from datetime import datetime

class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def make_sound(self):
        raise NotImplementedError("Subclass must implement abstract method")

class Dog(Animal):
    def make_sound(self):
        return "Woof!"

class Cat(Animal):
    def make_sound(self):
        return "Meow!"

def save_to_file(data, filename):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file)
    except IOError as e:
        print(f"Error writing to file: {e}")

def load_from_file(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except IOError as e:
        print(f"Error reading from file: {e}")
        return None

def generate_random_number(start, end):
    return random.randint(start, end)

def main():
    animals = [Dog("Buddy", 3), Cat("Whiskers", 2)]
    for animal in animals:
        print(f"{animal.name} says {animal.make_sound()}")

    data = {"animals": [{"name": animal.name, "age": animal.age} for animal in animals]}
    save_to_file(data, "animals.json")

    loaded_data = load_from_file("animals.json")
    if loaded_data:
        print("Loaded data:", loaded_data)

    random_number = generate_random_number(1, 100)
    print("Random number:", random_number)

    current_time = datetime.now()
    print("Current time:", current_time)

    if os.path.exists("animals.json"):
        print("File 'animals.json' exists.")
    else:
        print("File 'animals.json' does not exist.")

if __name__ == "__main__":
    main()
```