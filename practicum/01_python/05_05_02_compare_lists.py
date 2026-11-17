"""Сравните два списка и верните сообщение о результате сравнения.

Функция compare_sequences() принимает два списка и сравнивает их
операторами сравнения последовательностей. Для большего списка
верните f-строку «Список <sequence> больше.», подставив сам список.
Если списки равны, верните «Списки равны.». Вызовите функцию
с исходными sequence_1 и sequence_2 и напечатайте результат.
"""

sequence_1 = [69, 59, 57, 60, 63, 44, 46, 69]
sequence_2 = [33, 73, 50, 25, 36, 68, 52, 76]


def compare_sequences(sequence_1, sequence_2):
    if sequence_1 > sequence_2:
        return f"Список {sequence_1} больше."
    if sequence_2 > sequence_1:
        return f"Список {sequence_2} больше."
    return "Списки равны."


print(compare_sequences(sequence_1, sequence_2))
