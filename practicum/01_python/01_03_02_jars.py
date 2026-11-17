"""Типизация и типы данных — количество заготовок.

Даны berry_jars = 25 и vegetables_jars = '12'. Вычислите общее
количество банок в quantity_of_jars и соберите строку оператором +:
«Заготовлено 25 банок с ягодами и 12 банок с овощами.
Всего заготовлено 37 банок.» Между предложениями один пробел.
"""

berry_jars = 25
vegetables_jars = "12"
quantity_of_jars = berry_jars + int(vegetables_jars)
print(
    "Заготовлено "
    + str(berry_jars)
    + " банок с ягодами и "
    + vegetables_jars
    + " банок с овощами. Всего заготовлено "
    + str(quantity_of_jars)
    + " банок."
)
