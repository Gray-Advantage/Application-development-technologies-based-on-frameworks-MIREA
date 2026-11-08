"""Представления страниц переходов по коротким ссылкам."""

from datetime import date

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models.clicks import Click, find_click_by_id
from db.repository import load_data


def build_click_row(click: Click, today: date) -> dict:
    """Подготовить данные перехода и состояние его ссылки для шаблона."""
    return {
        "click": click,
        "state": click.link.get_state(today),
        "available": click.link.is_available(today),
    }


def clicks(request: HttpRequest) -> HttpResponse:
    """Страница /clicks/: список переходов из data/clicks.json."""
    _, _, clicks_list = load_data()
    today = date.today()

    context = {
        "rows": [build_click_row(click, today) for click in clicks_list],
    }
    return render(request, "clicks/click_list.html", context)


def click_detail(request: HttpRequest, click_id: int) -> HttpResponse:
    """Страница /clicks/<int:click_id>/: карточка одного перехода."""
    _, _, clicks_list = load_data()
    click = find_click_by_id(clicks_list, click_id)

    row = None
    if click is not None:
        row = build_click_row(click, date.today())

    context = {"row": row}
    return render(
        request,
        "clicks/click_detail.html",
        context,
        status=404 if click is None else 200,
    )
