"""Определите общие и уникальные овощи в двух огородах.

В first_garden растут помидоры, огурцы и морковь, в second_garden —
перец, помидоры и лук. Сохраните в common_vegetables множество овощей,
которые растут в обоих огородах; в only_first_garden — овощи только
первого огорода; в only_second_garden — овощи только второго.
Напечатайте результаты с сообщениями «Овощи, растущие и в первом,
и во втором огороде:», «Овощи, растущие только в первом огороде:»,
«Овощи, растущие только во втором огороде:» соответственно.
"""

first_garden = {"помидоры", "огурцы", "морковь"}
second_garden = {"перец", "помидоры", "лук"}

common_vegetables = first_garden & second_garden
print("Овощи, растущие и в первом, и во втором огороде:", common_vegetables)

only_first_garden = first_garden - second_garden
print("Овощи, растущие только в первом огороде:", only_first_garden)

only_second_garden = second_garden - first_garden
print("Овощи, растущие только во втором огороде:", only_second_garden)
