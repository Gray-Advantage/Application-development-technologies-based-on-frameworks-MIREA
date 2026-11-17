"""
Напишите запрос, который подсчитает в таблице `ice_cream` среднюю стоимость тех
сортов мороженого, где в поле `category` стоит значение «Экзотическое».
Результат выведите в консоль.
"""

import sqlite3

con = sqlite3.connect("db.sqlite")
cur = con.cursor()

# Напишите SQL запрос в строке.
results = cur.execute("""
SELECT AVG(price)
FROM ice_cream
WHERE category = 'Экзотическое';
""")

for result in results:
    print(result)

con.close()
