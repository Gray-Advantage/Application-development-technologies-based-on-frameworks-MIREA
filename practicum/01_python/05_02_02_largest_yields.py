"""Найдите три самых больших урожая из кортежа apple_tree_yields.

Напишите reversed_sort(tpl), которая принимает неотсортированный
кортеж и возвращает кортеж из тех же элементов, отсортированных
по убыванию. Примените функцию сортировки и преобразуйте её результат
в кортеж. Вызовите reversed_sort(apple_tree_yields), сохраните результат
в result и напечатайте первые три значения на отдельных строках:
сначала наибольшее, затем второе и третье по величине.
"""

apple_tree_yields = (150, 210, 90, 120, 140, 190, 130, 150, 110, 200, 150)


def reversed_sort(tpl):
    return tuple(sorted(tpl, reverse=True))


result = reversed_sort(apple_tree_yields)
print(result[0])
print(result[1])
print(result[2])
