"""Верните список расстояний от начала грядки до каждого ряда.

Функция planting_plan(rows) принимает количество рядов. Первый ряд
расположен в двух метрах от начала грядки, каждый следующий — ещё
на два метра дальше. Задайте start и step, вычислите end и создайте
диапазон row_positions. Преобразуйте его в список и верните.
Напечатайте planting_plan(4): результат должен быть [2, 4, 6, 8].
"""


def planting_plan(rows):
    start = 2
    step = 2
    end = start + rows * step
    row_positions = range(start, end, step)
    return list(row_positions)


print(planting_plan(4))
