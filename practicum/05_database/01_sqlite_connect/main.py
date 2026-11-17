"""
Создаём и заполняем базу данных с мороженым на раз-два-три. Задание первое:
создайте из кода на Python базу данных SQLite. Файл должен называться
*db.sqlite*.
"""

import sqlite3

con = sqlite3.connect("db.sqlite")
con.close()
