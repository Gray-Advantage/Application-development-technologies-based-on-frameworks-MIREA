"""Простые типы данных — восстановление выражения.

Расставьте операторы между 2, 9, 4, 1 без изменения порядка чисел.
Переменная result должна равняться пяти, solve_expression возвращает True.
"""


def solve_expression():
    result = 2 + 9 // 4 + 1
    return result == 5


print("Верно посчитано?", solve_expression())
