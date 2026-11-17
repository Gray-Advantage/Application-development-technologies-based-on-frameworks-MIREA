"""Огород состоит из трёх участков, каждый содержит три грядки.

Создайте списковым включением список списков harvest. Каждый вложенный список
описывает участок и содержит три случайных целых веса урожая от 5 до 20 кг.
Функция total_harvest(harvest) должна вернуть общий вес урожая всех грядок.
Функция average_harvest_per_plot(harvest) должна вернуть список средних весов
урожая с одной грядки для каждого участка. Используйте функцию sum().
Например, для [[1, 2, 3], [3, 2, 4], [1, 1, 1]] общий урожай равен 18,
а список средних значений равен [2.0, 3.0, 1.0].
Напечатайте harvest, общий урожай и средние значения
с сообщениями из заготовки.
"""

import random

harvest = [[random.randint(5, 20) for _ in range(3)] for _ in range(3)]


def total_harvest(harvest):
    return sum([sum(plot) for plot in harvest])


def average_harvest_per_plot(harvest):
    return [sum(plot) / len(plot) for plot in harvest]


print("Урожай с каждой грядки на каждом участке:", harvest)
print("Общий урожай со всех участков:", total_harvest(harvest))
print("Средний урожай с каждого участка:", average_harvest_per_plot(harvest))
