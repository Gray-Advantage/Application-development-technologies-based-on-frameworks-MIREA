"""
В веб-проекте администратор может снимать с публикации какие-то записи, не
удаляя их из БД. За это в нашем проекте отвечает поле `is_published` в таблице
`ice_cream`. А чтобы отметить, какие сорта мороженого будут показаны на главной
странице проекта, а какие нет — понадобится поле `is_on_main`.

В таблицу `ice_cream` добавьте обязательные колонки `is_published` и
`is_on_main` типа INTEGER, в которых будет храниться значение 0 (в Python это
`False`) или 1 (в Python это `True`).
"""

import sqlite3

con = sqlite3.connect("db.sqlite")
cur = con.cursor()

cur.executescript("""
ALTER TABLE ice_cream ADD COLUMN is_published INTEGER NOT NULL;
ALTER TABLE ice_cream ADD COLUMN is_on_main INTEGER NOT NULL;
""")

con.close()
