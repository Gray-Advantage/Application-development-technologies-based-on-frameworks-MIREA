"""Практика циклов — фасовка пирожных.

print_pack_report печатает числа от starting_value до единицы включительно.
Для кратных трём и пяти выводится «расфасуем по 3 или по 5», только пяти
— «расфасуем по 5», только трём — «расфасуем по 3», иначе —
«не заказываем!». Формат строки: число, пробел, дефис, пробел, сообщение.
"""


def print_pack_report(starting_value):
    for number in range(starting_value, 0, -1):
        if number % 3 == 0 and number % 5 == 0:
            print(number, "- расфасуем по 3 или по 5")
        elif number % 5 == 0:
            print(number, "- расфасуем по 5")
        elif number % 3 == 0:
            print(number, "- расфасуем по 3")
        else:
            print(number, "- не заказываем!")


print_pack_report(31)
