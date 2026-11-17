"""Ветвление if else — площади грядок.

Измените аргументы одного из вызовов rectangle_area, чтобы условие
area_1 < area_2 стало истинным. Сохраните функцию и сообщения программы.
"""


def rectangle_area(length, width):
    return length * width


area_1 = rectangle_area(4, 10)
area_2 = rectangle_area(7, 7)

if area_1 < area_2:
    print("Площадь первой грядки меньше второй!")

print("Сравнение грядок завершено!")
