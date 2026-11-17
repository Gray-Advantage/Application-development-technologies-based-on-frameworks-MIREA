"""Дата и время — вывод дня и месяца.

Для birthday = datetime(1955, 6, 8, 23, 20, 0) сформируйте строку
только из дня и месяца с ведущими нулями, разделённых точкой.
Выведите результат с подписью «День рождения:».
"""

from datetime import datetime

birthday = datetime(1955, 6, 8, 23, 20, 0)
birthday_day_and_month = datetime.strftime(birthday, "%d.%m")
print("День рождения:", birthday_day_and_month)
