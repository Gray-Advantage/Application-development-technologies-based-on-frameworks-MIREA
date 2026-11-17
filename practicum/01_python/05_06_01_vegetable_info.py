"""Создайте словарь с сортами овощей и их урожайностью.

Функция create_vegetable_info() принимает три списка: названия овощей,
сорта и урожайность в кг/м². Верните vegetable_info: ключ — название
овоща, значение — кортеж (сорт, урожайность) из элементов с тем же
индексом. Например, для ['Ананасы'], ['Броненосец'], [3.1] результат
{'Ананасы': ('Броненосец', 3.1)}. Используйте zip() для объединения
последовательностей и dict() для создания словаря. Вызовите функцию
с тестовыми vegetables, varieties, yields и напечатайте результат.
"""


def create_vegetable_info(vegetables, varieties, yields):
    vegetable_info = dict(zip(vegetables, zip(varieties, yields)))
    return vegetable_info


vegetables = ["Помидоры", "Огурцы", "Баклажаны", "Перец", "Капуста"]
varieties = [
    "Красный куб",
    "Аллигатор",
    "Василёк",
    "Тропический закат",
    "Арктик",
]
yields = [6.5, 4.3, 2.8, 2.2, 3.5]

print(create_vegetable_info(vegetables, varieties, yields))
