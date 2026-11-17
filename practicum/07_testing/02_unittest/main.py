"""
В функции `bubble_sort()` применён алгоритм сортировки, который получил
название «метод пузырька»: элементы с меньшими значениями «всплывают» в списке,
как пузырьки в газировке, например.

С помощью библиотеки unittest протестируйте функцию `bubble_sort()`; проверьте,
корректно ли работает функция

- с неотсортированным списком чисел, состоящим из `int` и `float`;
- с пустым списком.
"""

import unittest


def bubble_sort(array: list[float]) -> list[float]:
    """Сортировка списка методом пузырька по возрастанию."""
    length = len(array)
    for bypass in range(1, length):
        for k in range(length - bypass):
            if array[k] > array[k + 1]:
                array[k], array[k + 1] = array[k + 1], array[k]
    return array


class TestBubbleSort(unittest.TestCase):
    """Тестируем функцию bubble_sort."""

    def test_int_float(self):
        # С несортированным списком чисел
        call = bubble_sort([3, -1.5, 0, 2.5, -2, 3])
        result = [-2, -1.5, 0, 2.5, 3, 3]
        self.assertEqual(
            call,
            result,
            "Функция bubble_sort некорректно работает со списком чисел",
        )

    def test_empty(self):
        # С пустым списком
        call = bubble_sort([])
        result = []
        self.assertEqual(
            call,
            result,
            "Функция bubble_sort некорректно работает с пустым списком",
        )
