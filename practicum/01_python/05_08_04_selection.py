"""Практика коллекций — выборка стандартного роста.

get_selection принимает уже отсортированный по возрастанию список.
Верните срез без первых и последних десяти процентов элементов.
Левую границу 10% и правую границу 90% вычислите через int.
Список может иметь произвольную длину.
"""


def get_selection(collection):
    left = int(len(collection) * 0.1)
    right = int(len(collection) * 0.9)
    return collection[left:right]


heights = [140.1, 150.3, 155, 160.4, 162.7, 163, 168.9, 170, 179.1, 180]
selection = get_selection(heights)
print("Выборка:", selection)
