"""Дата и время — количество дней между посевной и урожаем.

get_difference_in_days принимает две строки в формате
ГГГГ/ММ/ДД ЧЧ:ММ:СС, преобразует их в datetime и возвращает
количество целых дней от первой даты до второй. Для примера используйте
2019/05/10 11:26:31 и 2019/10/04 10:01:19.
"""

from datetime import datetime


def get_difference_in_days(datetime_str_1, datetime_str_2):
    pattern = "%Y/%m/%d %H:%M:%S"
    first = datetime.strptime(datetime_str_1, pattern)
    second = datetime.strptime(datetime_str_2, pattern)
    return (second - first).days


difference = get_difference_in_days(
    "2019/05/10 11:26:31", "2019/10/04 10:01:19"
)
print("От начала посевной до начала сбора урожая прошло", difference, "дней.")
