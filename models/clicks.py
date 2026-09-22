"""Класс перехода по ссылке и функции учёта переходов и статистики."""

from collections.abc import Iterable, Iterator
from datetime import date

from utils import format_date, get_next_id

from .links import Link, filter_available_links
from .users import User

POPULAR_CLICKS = 10
DEFAULT_SOURCE = "direct"
TOP_LINKS_LIMIT = 3
RECENT_CLICKS_LIMIT = 5


class Click:
    """Переход по короткой ссылке."""

    def __init__(
        self,
        click_id: int,
        link: Link,
        clicked_at: date,
        source: str,
    ) -> None:
        """Создать объект перехода."""
        self.id = click_id
        self.link = link
        self.clicked_at = clicked_at
        self.source = source

    def __str__(self) -> str:
        """Вернуть строковое представление перехода."""
        return (
            f"#{self.id} {format_date(self.clicked_at)} "
            f"{self.link.short_url} (источник: {self.source})"
        )


def register_click(
    clicks: list[Click],
    link: Link,
    clicked_at: date,
    source: str = "",
) -> Click:
    """Зарегистрировать переход по ссылке и добавить его в коллекцию.

    Если дата перехода раньше даты создания ссылки или ссылка
    недоступна (отключена или истекла), возбуждается ValueError.
    """
    if link.days_passed(clicked_at) < 0:
        raise ValueError("Дата перехода раньше даты создания ссылки")
    if not link.is_available(clicked_at):
        raise ValueError(
            f"Переход невозможен: ссылка {link.get_state(clicked_at)}"
        )

    click = Click(
        get_next_id(clicks),
        link,
        clicked_at,
        source.strip().lower() or DEFAULT_SOURCE,
    )
    clicks.append(click)
    return click


def iter_link_clicks(clicks: list[Click], link: Link) -> Iterator[Click]:
    """Выдавать по одному переходы по ссылке link."""
    for click in clicks:
        if click.link is link:
            yield click


def count_clicks_by(clicks: Iterable[Click], attribute: str) -> dict:
    """Посчитать переходы по значениям атрибута перехода.

    По атрибуту link считается количество переходов по каждой ссылке,
    по атрибуту source — по каждому источнику.
    """
    counts: dict[str, int] = {}

    for click in clicks:
        value = getattr(click, attribute)
        counts[value] = counts.get(value, 0) + 1
    return counts


def get_clicks_per_day(clicks_count: int, days_passed: int) -> float:
    """Вычислить среднее количество переходов в день."""
    if days_passed > 0:
        return clicks_count / days_passed
    return float(clicks_count)


def is_popular(link: Link, clicks_count: int, today: date) -> bool:
    """Проверить, что доступная ссылка набрала много переходов."""
    return clicks_count >= POPULAR_CLICKS and link.is_available(today)


def get_top_links(
    links: list[Link], clicks: list[Click], limit: int = TOP_LINKS_LIMIT
) -> list[tuple[Link, int]]:
    """Вернуть самые популярные ссылки в виде пар (ссылка, переходы)."""
    counts = count_clicks_by(clicks, "link")
    ranking = [(link, counts.get(link, 0)) for link in links]
    ranking.sort(key=lambda item: item[1], reverse=True)
    return ranking[:limit]


def get_total_stats(
    links: list[Link],
    users: list[User],
    clicks: list[Click],
    today: date,
) -> dict:
    """Собрать общую статистику сервиса."""
    return {
        "users": len(users),
        "links": len(links),
        "available": sum(1 for _ in filter_available_links(links, today)),
        "disabled": sum(1 for link in links if not link.is_active),
        "clicks": len(clicks),
        "sources": len({click.source for click in clicks}),
        "top_links": get_top_links(links, clicks),
    }


def show_link_stats(link: Link, clicks: list[Click], today: date) -> None:
    """Вывести подробные сведения и статистику по ссылке."""
    link_clicks = list(iter_link_clicks(clicks, link))
    clicks_count = len(link_clicks)
    clicks_per_day = get_clicks_per_day(clicks_count, link.days_passed(today))

    print(link)
    print(f"Владелец: {link.owner}")
    print(f"Дата создания: {format_date(link.created_at)}")
    print(f"Действует до: {format_date(link.expires_at)}")
    print(f"Осталось дней: {max(link.days_left(today), 0)}")
    print(f"Состояние: {link.get_state(today)}")
    print(f"Переходов: {clicks_count}")
    print(f"Переходов в день: {clicks_per_day:.2f}")
    if is_popular(link, clicks_count, today):
        print(f"Ссылка популярна: не менее {POPULAR_CLICKS} переходов")
    if not link_clicks:
        return

    print("Источники переходов:")
    sources = count_clicks_by(link_clicks, "source")
    ranked_sources = sorted(
        sources.items(), key=lambda item: item[1], reverse=True
    )
    for source, count in ranked_sources:
        print(f"  {source}: {count}")
    print("Последние переходы:")
    for click in link_clicks[-RECENT_CLICKS_LIMIT:]:
        print(f"  {click}")


def show_total_stats(stats: dict) -> None:
    """Вывести общую статистику сервиса."""
    print(f"Пользователей: {stats['users']}")
    print(f"Всего ссылок: {stats['links']}")
    print(f"Доступных ссылок: {stats['available']}")
    print(f"Отключённых ссылок: {stats['disabled']}")
    print(f"Всего переходов: {stats['clicks']}")
    print(f"Уникальных источников: {stats['sources']}")
    if not stats["top_links"]:
        return
    print("Самые популярные ссылки:")
    for place, (link, count) in enumerate(stats["top_links"], start=1):
        print(f"  {place}. {link.short_url} — {count}")
