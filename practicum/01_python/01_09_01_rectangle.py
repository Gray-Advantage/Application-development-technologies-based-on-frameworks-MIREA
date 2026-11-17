"""Чтобы оценить затраты на обслуживание огорода, необходимо уточнить его
размеры.

Предполагается, что огороды всегда прямоугольные.

Напишите две функции:

- функция `get_rectangle_area()` должна получить на вход длину и ширину
огорода и вернуть его площадь;
- функция `get_rectangle_perimeter()` должна получить на вход длину и ширину
огорода и вернуть его периметр.

Функции должны не печатать результат, а **возвращать** его.

В коде заготовлены значения длины и ширины. Вызовите функции
`get_rectangle_area()` и `get_rectangle_perimeter()` с аргументами `length`
и `width` и напечатайте результаты вызовов в таком формате (только числа
будут другие):

```bash
Площадь: 32
Периметр: 24
```
"""


def get_rectangle_area(length: int, width: int) -> int:
    return length * width


def get_rectangle_perimeter(length: int, width: int) -> int:
    return 2 * (length + width)


# Длина прямоугольника.
length = 5
# Ширина прямоугольника.
width = 10

print("Площадь:", get_rectangle_area(length, width))
print("Периметр:", get_rectangle_perimeter(length, width))
