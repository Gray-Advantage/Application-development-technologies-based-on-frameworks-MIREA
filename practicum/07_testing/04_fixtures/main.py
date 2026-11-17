"""
Напишите тесты на метод `divider()` класса `Calculator`.

Проверьте:

- правильно ли работает деление;
- выбрасывается ли исключение при делении на 0.
"""

import unittest


class Calculator:
    """Производит арифметические действия."""

    def divider(self, num1, num2):
        """Возвращает результат деления num1 / num2."""
        if num2 == 0:
            raise ZeroDivisionError("Не могу делить на ноль")
        return num1 / num2


class TestCalc(unittest.TestCase):
    """Тестируем Calculator."""

    def setUp(self):
        self.calculator = Calculator()

    def test_divider(self):
        act = self.calculator.divider(9, 2)
        self.assertEqual(act, 4.5, "Некорректный результат деления")

    def test_divider_zero_division(self):
        # Проверьте, что деление на 0 выбрасывает исключение
        with self.assertRaises(ZeroDivisionError):
            self.calculator.divider(9, 0)
