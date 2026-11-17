"""
Таблицы, которые вы создали, уже наполнены информацией. Получите из базы самые
дорогие сорта мороженого в каждой из категорий. Код для вывода результатов в
консоль уже подготовлен.

Выборка должна выглядеть так:

```
('название_мороженого_1', 'слаг_категории_1', цена_1)
('название_мороженого_2', 'слаг_категории_2', цена_2)
```

Выборка должна быть отсортирована по цене, от дорогого мороженого к дешёвому.
Считайте, что цены на мороженое не повторяются.
"""

import sqlite3

con = sqlite3.connect("db.sqlite")
cur = con.cursor()

results = cur.execute("""
SELECT ice_cream.title, categories.slug, MAX(ice_cream.price)
FROM ice_cream, categories
WHERE ice_cream.category_id = categories.id
GROUP BY categories.slug
ORDER BY ice_cream.price DESC;
""")

for result in results:
    print(result)

con.close()
