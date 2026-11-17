"""
В классе `Calculator` описан метод калькулятора `summ`, который должен
складывать числа. Если вызвать этот метод без аргументов, он вернёт None.

Напишите тесты, которые проверяют, что `summ` корректно считает сумму для
одного аргумента и для нескольких аргументов, а также возвращает `None`, если
не передано никаких аргументов.
"""

import unittest


class Calculator:
    """Производит арифметические действия."""

    def summ(self, *args):
        """
        Возвращает сумму принятых аргументов,
        если аргументов нет, возвращает None.
        """
        if len(args) == 0:
            return None
        return sum(args)


class TestCalc(unittest.TestCase):
    """Тестируем Calculator."""

    calc: Calculator

    @classmethod
    def setUpClass(cls) -> None:
        """Вызывается один раз перед запуском всех тестов класса."""
        cls.calc = Calculator()

    def test_summ(self) -> None:
        act = TestCalc.calc.summ(1, 2.5, -3)
        self.assertEqual(act, 0.5)

    def test_summ_no_argument(self) -> None:
        act = TestCalc.calc.summ()
        self.assertIsNone(act)

    def test_summ_one_argument(self) -> None:
        act = TestCalc.calc.summ(5)
        self.assertEqual(act, 5)
