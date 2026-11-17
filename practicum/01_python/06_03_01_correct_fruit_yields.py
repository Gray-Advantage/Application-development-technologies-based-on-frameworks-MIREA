"""На основе fruit_yields создайте список corrected_fruit_yields.

Каждое значение исходного списка увеличьте на 1.2.
Вместо цикла используйте единственную строку со списковым включением.
Напечатайте полученный список.
"""

fruit_yields = [164.8, 105.0, 124.3, 113.8]

corrected_fruit_yields = [yield_value + 1.2 for yield_value in fruit_yields]

print(corrected_fruit_yields)
