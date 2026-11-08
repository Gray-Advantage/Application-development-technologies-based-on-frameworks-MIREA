"""Фильтрация, сортировка и пагинация переходов."""

from datetime import date

from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from links.models import Link
from links.queries import click_list
from users.models import User
from .models import Click


def build_click_row(click: Click, today: date) -> dict:
    """Связанные объекты загружены через select_related."""
    return {
        "click": click,
        "state": click.link.get_state(today),
        "available": click.link.is_available(today),
    }


def clicks(request: HttpRequest) -> HttpResponse:
    """Q03/Q19: фильтры → сортировка → пагинация."""
    params = request.GET.dict()
    errors = []
    if params.get("date"):
        try:
            date.fromisoformat(params["date"])
        except ValueError:
            errors.append("Некорректная дата. Используйте ГГГГ-ММ-ДД.")
    if params.get("owner"):
        try:
            owner = int(params["owner"])
            if not 0 < owner <= 9223372036854775807:
                raise ValueError
        except ValueError:
            errors.append("Некорректный идентификатор владельца.")
    result = Click.objects.none() if errors else click_list(params)
    page = Paginator(result, 5).get_page(request.GET.get("page"))
    return render(
        request,
        "clicks/click_list.html",
        {
            "rows": [build_click_row(click, date.today()) for click in page],
            "page_obj": page,
            "error": " ".join(errors),
            "filters": params,
            "owners": User.objects.order_by("username"),
            "links": Link.objects.order_by("code"),
        },
    )


def click_detail(request: HttpRequest, click_id: int) -> HttpResponse:
    """Q20: переход со ссылкой и владельцем одним SQL-запросом."""
    click = get_object_or_404(
        Click.objects.select_related("link__owner"), pk=click_id
    )
    return render(
        request,
        "clicks/click_detail.html",
        {
            "row": build_click_row(click, date.today()),
        },
    )
