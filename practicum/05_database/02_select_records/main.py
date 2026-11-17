"""
В тренажёре в файле *db.sqlite* заготовлена база данных. Выведите из таблицы,
которая хранится в этой базе, значения столбцов `title` и `description` всех
записей.

Задача выполняется в коде в два шага:

1. Узнать название таблицы.
2. Вывести записи из этой таблицы.

В уроках не было примеров запроса для получения списка таблиц в БД SQLite;
найдите решение самостоятельно — поисковые системы вам помогут, но мы вам
немного подскажем: в SQLite есть служебная таблица [sqlite_master], в колонке
`tbl_name` она хранит названия всех таблиц, которые есть в базе. Сделайте
запрос к этой таблице и получите все значения поля `tbl_name`.

Используйте метод курсора [fetchall()], чтобы получить и присвоить нужное
значение переменной `table`.

[sqlite_master]:
    https://www.sqlite.org/vdbe.html

[fetchall()]:
    https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.fetchall
"""

import sqlite3

con = sqlite3.connect("db.sqlite")
cur = con.cursor()

# Напишите SQL запрос в строке.
cur.execute("""
    SELECT tbl_name
    FROM sqlite_master
    WHERE type = 'table' AND name NOT LIKE 'sqlite_%';

""")

table = cur.fetchall()[0][0]

# Напишите SQL запрос в строке.
results = cur.execute(f"""
    SELECT title, description
    FROM {table};
""")


for result in results:
    print(result)

con.close()
