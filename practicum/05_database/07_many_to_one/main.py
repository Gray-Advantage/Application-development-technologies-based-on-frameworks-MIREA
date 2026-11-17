"""
Сорта мороженого разделяются на группы — категории. Например, какие-то сорта
войдут в категорию «Экзотические», какие-то — в категорию «Классические»;
возможно, потом появится и категория «Не вздумай пробовать».

В каждой категории может быть несколько сортов мороженого, но каждое мороженое
может принадлежать лишь одной категории: это классический пример связи 1:M.

Нужно добавить категории в базу данных.

Допишите SQL-запрос:

1. Добавьте запрос, который создаст таблицу **categories** — в ней будут
  храниться типы мороженого.

    В таблице должно быть два обязательных поля:

    - `id` — уникальный идентификатор записи,
    - `slug` — обязательное текстовое поле; значение этого поля будет
      использоваться, например, для создания URL страницы, где будут
      отображаться все сорта из одной категории.
2. Свяжите таблицу **ice_cream** с таблицей **categories**: добавьте в
  **ice_cream** поле `category_id`, ссылающееся на PK в таблице **categories**.
  Связь — обязательна: не может быть мороженого без категории.
"""

import sqlite3

con = sqlite3.connect("db.sqlite")
cur = con.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS categories(
id INTEGER PRIMARY KEY,
slug TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ice_cream(
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
description TEXT,
price REAL NOT NULL,
category_id INTEGER NOT NULL,
FOREIGN KEY (category_id) REFERENCES categories(id)
);

""")

con.close()
