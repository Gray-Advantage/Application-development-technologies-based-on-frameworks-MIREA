"""Практика циклов — таблица умножения.

print_multiplication_table печатает все произведения чисел от 1 до 9
в формате «1 * 2 = 2». После девяти строк каждого блока напечатайте
десять дефисов. Функция ничего не возвращает.
"""


def print_multiplication_table():
    for first in range(1, 10):
        for second in range(1, 10):
            print(first, "*", second, "=", first * second)
        print("----------")


print_multiplication_table()
