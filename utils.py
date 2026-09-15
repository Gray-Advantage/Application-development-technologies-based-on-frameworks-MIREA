"""Вспомогательные функции: безопасный ввод и форматирование."""

from collections.abc import Iterable
from datetime import date, datetime

DATE_FORMAT = "%d.%m.%Y"
YES_ANSWERS = ("д", "да", "y", "yes")


def input_text(prompt: str, allow_empty: bool = False) -> str:
    """Запросить строку; пустой ввод повторяется, если он не разрешён."""
    while True:
        value = input(prompt).strip()
        if value or allow_empty:
            return value
        print("Значение не может быть пустым")


def input_int(
    prompt: str,
    min_value: int,
    max_value: int | None = None,
    default: int | None = None,
) -> int:
    """Запросить целое число не меньше min_value и не больше max_value.

    Если max_value не задан, верхняя граница не проверяется.
    При пустом вводе возвращается default, если он задан.
    При некорректном вводе запрос повторяется.
    """
    while True:
        raw_value = input(prompt).strip()
        if not raw_value and default is not None:
            return default
        try:
            value = int(raw_value)
        except ValueError:
            print("Введите целое число")
            continue
        if value < min_value:
            print(f"Введите число не меньше {min_value}")
        elif max_value is not None and value > max_value:
            print(f"Введите число не больше {max_value}")
        else:
            return value


def input_date(prompt: str, default: date) -> date:
    """Запросить дату в формате ДД.ММ.ГГГГ; при пустом вводе — default.

    При некорректном формате запрос повторяется.
    """
    while True:
        raw_value = input(prompt).strip()
        if not raw_value:
            return default
        try:
            return datetime.strptime(raw_value, DATE_FORMAT).date()
        except ValueError:
            print("Введите дату в формате ДД.ММ.ГГГГ")


def input_yes_no(prompt: str) -> bool:
    """Запросить подтверждение действия."""
    return input(prompt).strip().lower() in YES_ANSWERS


def format_date(value: date) -> str:
    """Преобразовать дату в строку формата ДД.ММ.ГГГГ."""
    return value.strftime(DATE_FORMAT)


def get_next_id(items: Iterable) -> int:
    """Вернуть следующий свободный идентификатор объекта."""
    return max((item.id for item in items), default=0) + 1
