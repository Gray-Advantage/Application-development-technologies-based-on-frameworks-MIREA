"""Представления страниц коротких ссылок."""

from datetime import date

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models.clicks import count_clicks_by, get_clicks_per_day, is_popular
from models.links import Link, find_link_by_code
from db.repository import load_data, select, statistics


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
    _, links_list, clicks_list = load_data()
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
    _, links_list, clicks_list = load_data()
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


def available(request: HttpRequest) -> HttpResponse:
    """Поиск ссылок, доступных в выбранный день, по коду или URL."""
    value = request.GET.get("date", date.today().isoformat())
    error = ""
    try:
        day = date.fromisoformat(value)
    except ValueError:
        day = date.today()
        error = "Некорректная дата. Используйте ГГГГ-ММ-ДД."
    query = request.GET.get("q", "").strip()
    available_codes = {
        row["code"] for row in select("available", {"date": day.isoformat()})
    }
    found_codes = {
        row["code"] for row in select("search", {"query": f"%{query}%"})
    }
    _, links_list, clicks_list = load_data()
    counts = count_clicks_by(clicks_list, "link")
    cards = [
        build_link_card(link, counts.get(link, 0), day)
        for link in links_list
        if link.code in available_codes & found_codes
    ]
    return render(
        request,
        "links/available.html",
        {
            "cards": [] if error else cards,
            "date": value,
            "q": query,
            "error": error,
        },
    )


def stats(request: HttpRequest) -> HttpResponse:
    """Статистика SQL: агрегаты, группировки и ссылки без переходов."""
    return render(request, "links/statistics.html", statistics())
