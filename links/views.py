"""Представления страниц коротких ссылок."""

from datetime import date

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models.clicks import count_clicks_by, get_clicks_per_day, is_popular
from models.links import Link, find_link_by_code
from storage import load_all


def build_link_card(link: Link, clicks_count: int, today: date) -> dict:
    """Подготовить данные ссылки для шаблона карточки.

    Предметная логика остаётся в Python: методы объекта вызываются здесь,
    а шаблон только выводит готовые значения.
    """
    return {
        "link": link,
        "clicks": clicks_count,
        "state": link.get_state(today),
        "available": link.is_available(today),
        "days_left": max(link.days_left(today), 0),
        "per_day": get_clicks_per_day(clicks_count, link.days_passed(today)),
        "popular": is_popular(link, clicks_count, today),
    }


def links(request: HttpRequest) -> HttpResponse:
    """Страница /links/: список ссылок из data/links.json."""
    _, links_list, clicks_list = load_all(settings.DATA_DIR)
    today = date.today()
    counts = count_clicks_by(clicks_list, "link")

    context = {
        "cards": [
            build_link_card(link, counts.get(link, 0), today)
            for link in links_list
        ],
    }
    return render(request, "links/link_list.html", context)


def link_detail(request: HttpRequest, code: str) -> HttpResponse:
    """Страница /links/<slug:code>/: карточка ссылки и её статистика."""
    _, links_list, clicks_list = load_all(settings.DATA_DIR)
    link = find_link_by_code(links_list, code)

    card = None
    if link is not None:
        counts = count_clicks_by(clicks_list, "link")
        card = build_link_card(link, counts.get(link, 0), date.today())

    context = {"card": card}
    return render(
        request,
        "links/link_detail.html",
        context,
        status=404 if link is None else 200,
    )
