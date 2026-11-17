"""
Из таблицы `ice_cream` базы данных в файле `db.sqlite` получите значение поля
`title` тех записей, у которых значения поля `is_published` и `is_on_main`
равны 1 (в Python это значение соответствует `True`).
"""

import sqlite3

con = sqlite3.connect("db.sqlite")
cur = con.cursor()

# Напишите SQL запрос в строке.
results = cur.execute("""
SELECT title
FROM ice_cream
WHERE is_published = 1 AND is_on_main = 1;
""")


for result in results:
    print(result)


con.close()
