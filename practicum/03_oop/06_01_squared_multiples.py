"""Создайте генераторное выражение квадратов чисел numbers, кратных 3.

Распечатайте сумму квадратов. Для [1, 3, 4, 6, 9, 11] результат равен 126,
а для [1, 4, 11] результат равен 0.
"""

numbers = [1, 3, 4, 6, 9, 11]

squared_multiples = (number**2 for number in numbers if number % 3 == 0)

print(sum(squared_multiples))
