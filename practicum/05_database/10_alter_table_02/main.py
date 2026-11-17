"""
В таблице `ice_cream` переименуйте колонку `description`. Новое название должно
быть `specification`.
"""

import sqlite3

con = sqlite3.connect("db.sqlite")
cur = con.cursor()

cur.executescript("""
ALTER TABLE ice_cream RENAME COLUMN description TO specification;
""")

con.close()
