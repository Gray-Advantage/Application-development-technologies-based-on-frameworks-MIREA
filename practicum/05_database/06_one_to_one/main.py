"""
В метод `cur.executescript()`, который создаёт таблицу **ice_cream**, добавьте
ещё один запрос, который создаст таблицу **wrappers** — в ней будут храниться
названия обёрток для мороженого.

В таблице **wrappers** должны быть два поля. Название обёртки должно храниться
в текстовом поле `title`.

Измените запрос, создающий таблицу **ice_cream**: добавьте в таблицу поле
`wrapper_id` так, чтобы записи из таблицы **ice_cream** могли ссылаться на одну
из записей в таблице **wrappers.**

У каждого мороженого может быть одна уникальная обёртка. Два разных мороженых
не могут ссылаться на одну обёртку.

У некоторых сортов мороженого может и не быть обёртки, так что связь — не
обязательна; в таблице **ice_cream** значение поля, ссылающегося на таблицу
**wrappers**, может быть `NULL`.
"""

import sqlite3

con = sqlite3.connect("db.sqlite")

cur = con.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS wrappers(
id INTEGER PRIMARY KEY,
title TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ice_cream(
id INTEGER PRIMARY KEY,
title TEXT,
description TEXT,
wrapper_id INTEGER UNIQUE,
FOREIGN KEY (wrapper_id) REFERENCES wrappers(id)
);
""")
con.close()
