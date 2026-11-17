"""Рассчитайте общий вес овощей и оценённую стоимость урожая.

Функция calc() принимает три параметра: количество корзин, вес овощей
в одной корзине в килограммах и стоимость овощей за один килограмм.
Функция должна вернуть два значения: общий вес и стоимость урожая.
Исходные данные: baskets = 462, average_weight = 25, price_per_kg = 175.
Вызовите функцию с этими данными и напечатайте результат с помощью
f-строки в формате «Общий вес урожая: <вес> кг. Оценённая стоимость
урожая: <стоимость>.». Всё сообщение выводится в одной строке.
"""

baskets = 462
average_weight = 25
price_per_kg = 175


def calc(baskets, average_weight, price_per_kg):
    total_weight = baskets * average_weight
    total_cost = total_weight * price_per_kg
    return total_weight, total_cost


total_weight, total_cost = calc(baskets, average_weight, price_per_kg)
print(
    f"Общий вес урожая: {total_weight} кг. "
    f"Оценённая стоимость урожая: {total_cost}."
)
