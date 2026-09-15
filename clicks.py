"""Функции для учёта переходов по ссылкам и расчёта статистики."""

from collections.abc import Iterable, Iterator
from datetime import date

from links import filter_active_links, get_days_passed, is_link_active
from utils import get_next_id

POPULAR_CLICKS = 10
DEFAULT_SOURCE = "direct"
TOP_LINKS_LIMIT = 3


def register_click(
    links: dict[str, dict],
    clicks: list[dict],
    code: str,
    clicked_at: date,
    source: str = "",
) -> dict:
    """Зарегистрировать переход по короткой ссылке.

    Если ссылки нет, возбуждается KeyError. Если дата перехода раньше
    даты создания ссылки или срок действия истёк — ValueError.
    """
    link = links[code]
    if get_days_passed(link, clicked_at) < 0:
        raise ValueError("Дата перехода раньше даты создания ссылки")
    if not is_link_active(link, clicked_at):
        raise ValueError("Срок действия ссылки истёк")

    click = {
        "id": get_next_id(clicks),
        "code": code,
        "clicked_at": clicked_at.isoformat(),
        "source": source.strip().lower() or DEFAULT_SOURCE,
    }
    clicks.append(click)
    return click


def iter_link_clicks(clicks: list[dict], code: str) -> Iterator[dict]:
    """Выдавать по одному переходы по ссылке с кодом code."""
    for click in clicks:
        if click["code"] == code:
            yield click


def count_by_field(records: Iterable[dict], field: str) -> dict[str, int]:
    """Посчитать, сколько раз встречается каждое значение поля field."""
    counts = {}
    for record in records:
        value = record[field]
        counts[value] = counts.get(value, 0) + 1
    return counts


def get_clicks_per_day(clicks_count: int, days_passed: int) -> float:
    """Вычислить среднее количество переходов в день."""
    if days_passed > 0:
        return clicks_count / days_passed
    return float(clicks_count)


def is_popular(clicks_count: int, days_left: int) -> bool:
    """Проверить, что активная ссылка набрала много переходов."""
    return clicks_count >= POPULAR_CLICKS and days_left > 0


def get_top_links(
    links: dict[str, dict], clicks: list[dict], limit: int = TOP_LINKS_LIMIT
) -> list[tuple[str, int]]:
    """Вернуть самые популярные ссылки в виде пар (код, переходы)."""
    counts = count_by_field(clicks, "code")
    ranking = [(code, counts.get(code, 0)) for code in links]
    ranking.sort(key=lambda item: item[1], reverse=True)
    return ranking[:limit]


def get_total_stats(
    links: dict[str, dict], clicks: list[dict], today: date
) -> dict:
    """Собрать общую статистику сервиса."""
    return {
        "links": len(links),
        "active_links": sum(1 for _ in filter_active_links(links, today)),
        "clicks": len(clicks),
        "sources": len({click["source"] for click in clicks}),
        "top_links": get_top_links(links, clicks),
    }


def delete_link_clicks(clicks: list[dict], code: str) -> int:
    """Удалить все переходы по ссылке и вернуть их количество.

    Список clicks изменяется на месте, поэтому изменения видны
    в вызывающем коде.
    """
    remaining = [click for click in clicks if click["code"] != code]
    removed_count = len(clicks) - len(remaining)
    clicks[:] = remaining
    return removed_count
