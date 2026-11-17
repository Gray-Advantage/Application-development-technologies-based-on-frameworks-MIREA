"""
В базе данных *db.sqlite* создайте таблицу **ice_cream** с полями `title`,
`description` и `category`. Все поля должны хранить данные типа «строка».

- Для всех полей таблицы укажите тип данных: `TEXT`.
- Не забудьте закрыть соединение с базой данных через `con.close()`
"""

import sqlite3

con = sqlite3.connect("db.sqlite")
cur = con.cursor()

cur.execute("""
CREATE TABLE ice_cream(
title TEXT,
description TEXT,
category TEXT
);
""")

con.close()
