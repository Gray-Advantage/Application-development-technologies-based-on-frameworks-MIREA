"""
В предыдущей задаче вы создали таблицы, а мы уже наполнили их данными.

Сделайте запрос к связанным таблицам и получите выборку вида `название
мороженого, название обёртки`.

В выборке должны быть только те сорта мороженого, обёртка которых начинается на
букву «Б».
"""

import sqlite3

con = sqlite3.connect("db.sqlite")

cur = con.cursor()

results = cur.execute("""
SELECT ice_cream.title, wrappers.title
FROM ice_cream, wrappers
WHERE ice_cream.wrapper_id = wrappers.id AND wrappers.title LIKE 'Б%';
""")

for result in results:
    print(result)

con.close()
