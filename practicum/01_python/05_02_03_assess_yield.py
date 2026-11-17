"""Вычислите вес урожая и верните его оценку из assess_yield().

Функция принимает количество растений number_of_plants и средний вес
урожая с растения average_weight в граммах. Верните кортеж: общий вес
в килограммах и сообщение. Если вес строго больше 100 кг, сообщение
«Ожидается отличный урожай.»; иначе, если строго больше 50 кг, —
«Ожидается хороший урожай.»; иначе, если больше нуля, —
«Урожай будет так себе.»; в остальных случаях — «Урожая не будет.».
Распакуйте результат assess_yield(50, 200) в total_weight и rating.
Напечатайте строку «<вес> кг. <сообщение>», сохранив пробелы и точки.
Например: «1.5 кг. Урожай будет так себе.».
"""


def assess_yield(number_of_plants, average_weight):
    total_weight = number_of_plants * average_weight / 1000
    if total_weight > 100:
        rating = "Ожидается отличный урожай."
    elif total_weight > 50:
        rating = "Ожидается хороший урожай."
    elif total_weight > 0:
        rating = "Урожай будет так себе."
    else:
        rating = "Урожая не будет."
    return total_weight, rating


total_weight, rating = assess_yield(50, 200)
print(total_weight, "кг.", rating)
