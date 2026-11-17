"""Дважды вызовите say_to_all(func, sequence), используя lambda-функции.

Первый вызов печатает для каждого имени из people строку Привет, <имя>!
Второй вызов печатает для каждого имени строку До завтра, <имя>!
Сначала должны появиться все шесть приветствий, затем все шесть прощаний.
"""

people = ["Антон", "Соня", "Коля", "Женя", "Тоня", "Стёпа"]


def say_to_all(func, sequence):
    for item in sequence:
        func(item)


say_to_all(lambda name: print(f"Привет, {name}!"), people)
say_to_all(lambda name: print(f"До завтра, {name}!"), people)
