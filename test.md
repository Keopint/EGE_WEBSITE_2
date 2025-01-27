# Заголовок 1
## Заголовок 2
### Заголовок 3

Html код: <h1> Hello world! </h1>

*курсив* и **жирный** текст

sdkjfsdjkf
dslkfjsdlkjf
dlskjflsdf

ldksfjklsdjfklsdjflksdjfkls

Latex: Some complex formula: $$P(|S - E[S]| \ge t) \le 2 \exp \left( -\frac{2 t^2 n^2}{\sum_{i = 1}^n (b_i - a_i)^2} \right).$$

Latex: These are centered formulas: $$x,$$ $$a_i^2 + b_i^2 \le a_{i+1}^2.$$ Afterwards...

```
def formatcode(code: str) -> str:
    t = tokenize_code(code)
    if t is None:
        return "Syntax error" + code
    code = untokenize_code(t)
    return code
```

1. Первый элемент
2. Второй элемент

* Первый элемент
* Второй элемент

[Google](https://www.google.com)

![Пример изображения](https://expositions.nlr.ru/Mayakovsky/images/6_12.jpg)

[[https://rutube.ru/video/7fb1631331c40cef9efce0b5f53f05d4/?r=wd]]

> Это цитата 

Спецсимволы: \n \s \t

<iframe width="720" height="405" src="https://rutube.ru/play/embed/7fb1631331c40cef9efce0b5f53f05d4/" frameBorder="0" allow="clipboard-write; autoplay" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>

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