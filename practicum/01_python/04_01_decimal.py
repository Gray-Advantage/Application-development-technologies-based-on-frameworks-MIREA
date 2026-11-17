"""Decimal — площадь и объём эллиптического пруда.

Импортируйте Decimal, getcontext и число pi. Полуоси пруда 2.5 и 1.75 м,
глубина 0.35 м. Все значения перед расчётом приведите к Decimal через
строки; установите точность 10 значащих цифр. get_ellipse_area принимает
две полуоси и возвращает площадь. Объём вычислите вне функции.
Напечатайте «Площадь пруда: <площадь> кв.м.» и
«Количество воды для наполнения пруда: <объём> куб.м.».
"""

from decimal import Decimal, getcontext
from math import pi as math_pi

getcontext().prec = 10


def get_ellipse_area(long_axis, short_axis):
    return pi * long_axis * short_axis


pi = Decimal(str(math_pi))
long_axis = Decimal("2.5")
short_axis = Decimal("1.75")
depth = Decimal("0.35")
area = get_ellipse_area(long_axis, short_axis)
volume = area * depth
print(f"Площадь пруда: {area} кв.м.")
print(f"Количество воды для наполнения пруда: {volume} куб.м.")
