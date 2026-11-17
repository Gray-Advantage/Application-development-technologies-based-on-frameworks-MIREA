"""Чай в термосе имеет начальную температуру 85 °C.

Ежеминутно он остывает на случайное целое число градусов от 1 до 3.
Напишите цикл while, работающий, пока температура выше 60 °C.
На каждой итерации печатайте две строки:
Прошла минута.
Чай остыл ещё на <значение_1> °C. Текущая температура: <значение_2> °C
После завершения цикла напечатайте: Время пить чай!
"""

from random import randint

current_temperature = 85

while current_temperature > 60:
    temperature_drop = randint(1, 3)
    current_temperature -= temperature_drop
    print("Прошла минута.")
    print(
        f"Чай остыл ещё на {temperature_drop} °C. "
        f"Текущая температура: {current_temperature} °C"
    )

print("Время пить чай!")
