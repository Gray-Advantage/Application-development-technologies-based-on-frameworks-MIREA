"""
В тренажёре заготовлена база данных в файле *db.sqlite*. Она содержит таблицу с
именем `ice_cream`. Цены хранятся в поле `price`.

Узнайте среднюю цену мороженого для каждой категории (по столбцу `category`) и
выведите в консоль результат в виде `(категория, средняя_цена)`.

Если потребуется повнимательнее рассмотреть структуру таблицы — выполните
запрос `PRAGMA table_info(ice_cream);`.
"""

import sqlite3

con = sqlite3.connect("db.sqlite")
cur = con.cursor()

# Напишите SQL запрос в строке.
results = cur.execute("""
SELECT category, AVG(price)
FROM ice_cream
GROUP BY category;
""")

for result in results:
    print(result)

con.close()
