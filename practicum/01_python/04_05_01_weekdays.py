"""Практика дат — сегодняшний и послезавтрашний дни недели.

get_weekday_name принимает номер дня недели от нуля до шести и возвращает
русское название строчными буквами. get_day_after_tomorrow принимает
дату ГГГГ-ММ-ДД и возвращает сообщение «Сегодня <дата>, <день недели>,
а послезавтра - <день недели через два дня>.». Используйте datetime,
timedelta, weekday и вызовы вспомогательной функции.
"""

from datetime import datetime, timedelta


def get_weekday_name(weekday_number):
    if weekday_number == 0:
        return "понедельник"
    elif weekday_number == 1:
        return "вторник"
    elif weekday_number == 2:
        return "среда"
    elif weekday_number == 3:
        return "четверг"
    elif weekday_number == 4:
        return "пятница"
    elif weekday_number == 5:
        return "суббота"
    else:
        return "воскресенье"


def get_day_after_tomorrow(date_string):
    now = datetime.strptime(date_string, "%Y-%m-%d")
    now_weekday = get_weekday_name(now.weekday())
    day_after_tomorrow = now + timedelta(days=2)
    day_after_tomorrow_weekday = get_weekday_name(day_after_tomorrow.weekday())
    return (
        f"Сегодня {date_string}, {now_weekday}, "
        f"а послезавтра - {day_after_tomorrow_weekday}."
    )


print(get_day_after_tomorrow("2024-01-01"))
print(get_day_after_tomorrow("2024-01-02"))
print(get_day_after_tomorrow("2024-01-03"))
print(get_day_after_tomorrow("2024-01-04"))
print(get_day_after_tomorrow("2024-01-05"))
print(get_day_after_tomorrow("2024-01-06"))
