"""Практика по теме — случайное количество пельменей.

Импортируйте randint из random как rnd. Функция
get_dumplings_recommendation должна возвращать целое число от 10 до 20
включительно. За пределами функции выведите сообщение
«Оптимальным количеством пельменей на сегодня будет <число>».
"""

from random import randint as rnd


def get_dumplings_recommendation():
    return rnd(10, 20)


print(
    "Оптимальным количеством пельменей на сегодня будет",
    get_dumplings_recommendation(),
)
