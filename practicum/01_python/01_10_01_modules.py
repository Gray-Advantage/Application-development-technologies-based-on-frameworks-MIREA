"""Модули в Python — случайное число и факториал.

Импортируйте factorial из math под именем fact, randint из random
под именем rnd. Получите случайное число от 1 до 10 включительно
в value, вычислите его факториал в result и напечатайте значения
в формате «Факториал 5 равен 120». После импортов оставьте две строки.
"""

from math import factorial as fact
from random import randint as rnd

value = rnd(1, 10)
result = fact(value)
print("Факториал", value, "равен", result)
