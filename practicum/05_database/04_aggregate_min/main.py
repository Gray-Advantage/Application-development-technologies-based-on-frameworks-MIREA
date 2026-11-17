"""
В тренажёре заготовлен файл c базой данных `db.sqlite` с таблицей `ice_cream`.

Поля таблицы:

- `is_published`, тип INTEGER (допустимые значения — 0 и 1; в Python это поле
  будет интерпретировано как `bool`)
- `is_on_main`, тип INTEGER (допустимые значения — 0 и 1; в Python это поле
  будет интерпретировано как `bool`)
- `title`, тип TEXT
- `description`, тип TEXT
- `category`, тип TEXT
- `price`, тип REAL

Напишите запрос, который найдёт стоимость самого дешёвого мороженого. Цены
хранятся в поле `price` таблицы `ice_cream`. Результат выведите в консоль.
"""

import sqlite3

con = sqlite3.connect("db.sqlite")
cur = con.cursor()

# Напишите SQL запрос в строке.
results = cur.execute("""
SELECT MIN(price)
FROM ice_cream;
""")


for result in results:
    print(result)

con.close()
