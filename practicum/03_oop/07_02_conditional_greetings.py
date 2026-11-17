"""Измените lambda-функцию, передаваемую в say_to_all(), для списка people.

Для имён, начинающихся с кириллической буквы «С», печатайте Здравствуй, <имя>!
Для остальных печатайте Привет, <имя>! Сохраните исходный порядок имён.
"""

people = ["Антон", "Соня", "Коля", "Женя", "Тоня", "Стёпа"]


def say_to_all(func, sequence):
    for item in sequence:
        func(item)


say_to_all(
    lambda name: print(
        f"Здравствуй, {name}!" if name.startswith("С") else f"Привет, {name}!"
    ),
    people,
)
