"""
К мороженому может прилагаться *топпинг* — какая-то добавка, которая делает
мороженое ещё вкуснее (даже если вкуснее некуда).

Есть множество топпингов, их названия хранятся в таблице `toppings`.

Свяжите таблицы `ice_cream` и `toppings` через промежуточную таблицу
`ice_cream_toppings`  так, чтобы у мороженого могло быть несколько топпингов, а
могло бы не быть вовсе. У разных сортов мороженого могут быть одинаковые
топпинги.

В промежуточной таблице обязательно создайте колонку с первичным ключом.

Ключ в промежуточной таблице, связывающей `ice_cream` и `toppings`, **не должен
быть композитным**. Связь мороженого и топпинга — это неуникальная комбинация:
к одному мороженому можно привязать не один, а два, пять или десять
**одинаковых** топпингов.

Поэтому в таблице обязательно нужна колонка `id PRIMARY KEY`.

При выполнения задания не изменяйте прекод.
"""

import sqlite3

con = sqlite3.connect("db.sqlite")
cur = con.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS toppings(
id INTEGER PRIMARY KEY,
title TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ice_cream(
id INTEGER PRIMARY KEY,
title TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ice_cream_toppings(
id INTEGER PRIMARY KEY,
ice_cream_id INTEGER NOT NULL,
topping_id INTEGER NOT NULL,
FOREIGN KEY (ice_cream_id) REFERENCES ice_cream(id),
FOREIGN KEY (topping_id) REFERENCES toppings(id)
);
""")

con.close()
