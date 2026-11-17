"""
В тренажёре заготовлена база данных в файле `db.sqlite` с таблицей `ice_cream`.
Получите из этой таблицы результирующую выборку, которая

- содержит две записи, начиная со второй.
- отсортирована по полю `title` в обратном алфавитном порядке,
- содержит значения столбцов `title` и `description` тех записей, у которых
  значение поля `is_published` равно 1 (Python воспринимает это значение как
  `True`)
"""

import sqlite3

con = sqlite3.connect("db.sqlite")
cur = con.cursor()

# Напишите SQL запрос в строке.
results = cur.execute("""
SELECT title, description
FROM ice_cream
WHERE is_published = 1
ORDER BY title DESC
LIMIT 2 OFFSET 1;
""")


for result in results:
    print(result)

con.close()
