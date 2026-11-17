"""Практика по теме — параметры выбора количества пельменей.

Измените get_dumplings_recommendation: она принимает нижнюю и верхнюю
границы диапазона и возвращает случайное целое число между ними.
Сообщение о рекомендуемом количестве оставьте прежним.
При вызове укажите границы, например 25 и 30.
"""

from random import randint as rnd


def get_dumplings_recommendation(lower_bound, upper_bound):
    return rnd(lower_bound, upper_bound)


print(
    "Оптимальным количеством пельменей на сегодня будет",
    get_dumplings_recommendation(25, 30),
)
