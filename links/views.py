"""Страницы ссылок через Django ORM."""

from datetime import date

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from models.clicks import POPULAR_CLICKS, get_clicks_per_day
from .models import Link
from .queries import available_links, link_list, statistics


def build_link_card(link: Link, today: date) -> dict:
    """Сохранить контекст карточки ПР6."""
    count = link.clicks_count
    per_day = get_clicks_per_day(count, link.days_passed(today))
    return {
        "link": link,
        "clicks": count,
        "state": link.get_state(today),
        "available": link.is_available(today),
        "days_left": max(link.days_left(today), 0),
        "per_day": per_day,
        "popular": count >= POPULAR_CLICKS and link.is_available(today),
    }


def links(request: HttpRequest) -> HttpResponse:
    """Q01: список ссылок с владельцем и числом переходов."""
    return render(
        request,
        "links/link_list.html",
        {
            "cards": [
                build_link_card(link, date.today()) for link in link_list()
            ],
        },
    )


def link_detail(request: HttpRequest, code: str) -> HttpResponse:
    """Q18: отдельный объект или 404."""
    link = get_object_or_404(link_list(), code=code)
    return render(
        request,
        "links/link_detail.html",
        {
            "card": build_link_card(link, date.today()),
        },
    )


def available(request: HttpRequest) -> HttpResponse:
    """Q02: доступные на дату ссылки с поиском по коду или URL."""
    value = request.GET.get("date", date.today().isoformat())
    error = ""
    try:
        day = date.fromisoformat(value)
    except ValueError:
        day = date.today()
        error = "Некорректная дата. Используйте ГГГГ-ММ-ДД."
    query = request.GET.get("q", "").strip()
    cards = (
        []
        if error
        else [
            build_link_card(link, day) for link in available_links(day, query)
        ]
    )
    return render(
        request,
        "links/available.html",
        {
            "cards": cards,
            "date": value,
            "q": query,
            "error": error,
        },
    )


def stats(request: HttpRequest) -> HttpResponse:
    """Q04–Q17: сводки и связанные данные."""
    return render(request, "links/statistics.html", statistics())
