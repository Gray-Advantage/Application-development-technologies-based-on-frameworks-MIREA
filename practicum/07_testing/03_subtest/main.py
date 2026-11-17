"""
Заходит как-то раз тестировщик в бар и заказывает `5` стаканов газировки; `0`
стаканов газировки; `0.33` стакана газировки; `-1.999999` стакана газировки;
`фываолдж` стаканов газировки.

Передайте параметры для тестирования в метод `test_bartender()` класса
`TestBar`.
"""

import unittest


def bartender(order):
    if isinstance(order, int) and order > 0:
        return order
    return "Извините, я не могу вас обслужить!"


class TestBar(unittest.TestCase):

    def test_bartender(self):
        rejection = "Извините, я не могу вас обслужить!"
        cases = (
            (5, 5),
            (0, rejection),
            (0.33, rejection),
            (-1.999999, rejection),
            ("фываолдж", rejection),
        )
        for order, expected in cases:
            with self.subTest(order=order):
                self.assertEqual(bartender(order), expected)
