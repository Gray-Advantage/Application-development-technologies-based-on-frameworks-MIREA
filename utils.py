"""Вспомогательные функции: безопасный ввод и форматирование."""

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
    max_value: int,
    default: int | None = None,
) -> int:
    """Запросить целое число из диапазона от min_value до max_value.

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
        if min_value <= value <= max_value:
            return value
        print(f"Введите число от {min_value} до {max_value}")


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


def format_date(iso_date: str) -> str:
    """Преобразовать дату из формата ГГГГ-ММ-ДД в ДД.ММ.ГГГГ."""
    return date.fromisoformat(iso_date).strftime(DATE_FORMAT)


def get_next_id(records: list[dict]) -> int:
    """Вернуть следующий свободный числовой идентификатор записи."""
    return max((record["id"] for record in records), default=0) + 1
