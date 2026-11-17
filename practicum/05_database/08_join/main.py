"""
В тренажёре подготовлена база данных с тремя таблицами:

- **ice_cream** — сорта мороженого;

    Поля:

    - id
    - title
    - description
    - price
    - category_id
    - wrapper_id
- **categories** — категории мороженого;

    Поля:

    - id
    - slug
- **wrappers** — перечень упаковок.

    Поля:

    - id
    - title

Таблицы **ice_cream** и **wrappers** связаны 1:1 через поле
`ice_cream.wrapper_id`; связь необязательна: у мороженого может и не быть
упаковки.

Таблицы **ice_cream** и **categories** связаны 1:1 через поле
`ice_cream.category_id`; связь обязательна.

Объедините таблицы через `JOIN` и получите из базы

- названия мороженого (поле `title` таблицы **ice_cream**),
- названия упаковок (поле `title` из таблицы **wrappers**) для тех сортов, у
  которых  в описании упаковки используется слово «праздник» или однокоренные
  слова: *отпраздновать*, *предпраздничный*, *праздность..*.

Результат вашей работы будет выведен в консоль: в прекоде всё для этого готово.

В решении задачи поможет поиск по маске.
"""

import sqlite3

con = sqlite3.connect("db.sqlite")
cur = con.cursor()

results = cur.execute("""
SELECT ice_cream.title,
       wrappers.title
FROM ice_cream
JOIN wrappers ON ice_cream.wrapper_id = wrappers.id
WHERE wrappers.title LIKE '%празд%'
;
""")

for result in results:
    print(result)

con.close()
