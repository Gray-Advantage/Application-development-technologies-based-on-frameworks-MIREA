"""Финальный проект спринта: приложение «Холодильник».

Реализуйте add(), add_by_note(), find(), get_amount() и get_expired().
Словарь goods хранит продукты: ключ — название, значение — список партий.
У каждой партии есть amount типа Decimal и expiration_date типа date
либо None, если срок годности не указан. Формат даты — YYYY-MM-DD.

add(items, title, amount, expiration_date=None) добавляет партию продукта,
создавая список для нового названия и преобразуя строку даты в date.
add_by_note(items, note) разбирает строку «название количество [дата]»:
название может состоять из нескольких слов, количество преобразуется
в Decimal, дата необязательна. Для добавления партии вызывайте add().
find(items, needle) возвращает список названий, содержащих needle,
без учёта регистра. get_amount(items, needle) использует find() и
возвращает суммарное количество всех партий всех найденных продуктов.
get_expired(items, in_advance_days=0) получает сегодняшнюю дату, прибавляет
указанное количество дней и возвращает список кортежей (название,
суммарное количество партий с датой не позднее вычисленной границы).
Партии без даты не учитываются.

Проверяйте функции явными вызовами без input(): новые и существующие
продукты, названия из нескольких слов, необязательная дата, вчерашняя,
завтрашняя дата и дата через сто лет. Проверяйте поиск и суммы партий.
"""

from datetime import date, datetime, timedelta
from decimal import Decimal

DATE_FORMAT = "%Y-%m-%d"

goods = {}


def add(items, title, amount, expiration_date=None):
    """Добавить партию с количеством Decimal и датой date либо None."""
    if title not in items:
        items[title] = []
    if isinstance(expiration_date, str):
        expiration_date = datetime.strptime(
            expiration_date, DATE_FORMAT
        ).date()
    batch = {
        "amount": Decimal(str(amount)),
        "expiration_date": expiration_date,
    }
    items[title].append(batch)


def add_by_note(items, note):
    """Разобрать название, количество и необязательную дату, вызвать add()."""
    parts = note.split()
    expiration_date = None
    try:
        datetime.strptime(parts[-1], DATE_FORMAT)
    except ValueError:
        pass
    else:
        expiration_date = parts.pop()
    amount = Decimal(parts.pop())
    title = " ".join(parts)
    add(items, title, amount, expiration_date)


def find(items, needle):
    """Вернуть список названий с подстрокой needle без учёта регистра."""
    found_titles = []
    for title in items:
        if needle.lower() in title.lower():
            found_titles.append(title)
    return found_titles


def get_amount(items, needle):
    """Найти названия через find() и сложить количества всех их партий."""
    total_amount = Decimal("0")
    for title in find(items, needle):
        for batch in items[title]:
            total_amount += batch["amount"]
    return total_amount


def get_expired(items, in_advance_days=0):
    """Суммировать просроченные партии по границе today + in_advance_days."""
    expiration_limit = date.today() + timedelta(days=in_advance_days)
    expired_products = []
    for title, batches in items.items():
        expired_amount = Decimal("0")
        for batch in batches:
            expiration_date = batch["expiration_date"]
            if expiration_date is not None:
                if expiration_date <= expiration_limit:
                    expired_amount += batch["amount"]
        if expired_amount > 0:
            expired_products.append((title, expired_amount))
    return expired_products


if __name__ == "__main__":
    today = date.today()
    yesterday = (today - timedelta(days=1)).strftime(DATE_FORMAT)
    tomorrow = (today + timedelta(days=1)).strftime(DATE_FORMAT)
    next_century = date(today.year + 100, 12, 31).strftime(DATE_FORMAT)

    add(goods, "Молоко", Decimal("1.5"), yesterday)
    add(goods, "Молоко", Decimal("2"), tomorrow)
    add(goods, "Рис", Decimal("0.5"))
    add_by_note(goods, "Рис 1.5")
    add_by_note(goods, f"Сыр твёрдый 0.3 {tomorrow}")
    add_by_note(goods, f"Молоко 0.5 {next_century}")

    assert find(goods, "МОЛ") == ["Молоко"]
    assert find(goods, "сыр") == ["Сыр твёрдый"]
    assert find(goods, "Хлеб") == []
    assert get_amount(goods, "мол") == Decimal("4.0")
    assert get_amount(goods, "рис") == Decimal("2.0")
    assert get_amount(goods, "Хлеб") == Decimal("0")
    assert get_expired(goods) == [("Молоко", Decimal("1.5"))]
    assert get_expired(goods, 1) == [
        ("Молоко", Decimal("3.5")),
        ("Сыр твёрдый", Decimal("0.3")),
    ]

    print("Найденные продукты:", find(goods, "мол"))
    print("Количество молока:", get_amount(goods, "мол"))
    print("Просроченные продукты:", get_expired(goods))
    print("Срок истекает не позднее завтра:", get_expired(goods, 1))
