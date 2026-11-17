"""Фильтрация, сортировка и пагинация переходов."""

from datetime import date

from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from links.queries import click_list
from .forms import ClickFilterForm
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
    form = ClickFilterForm(request.GET)
    result = (
        click_list(form.query_params())
        if form.is_valid()
        else Click.objects.none()
    )
    page = Paginator(result, 5).get_page(request.GET.get("page"))
    return render(
        request,
        "clicks/click_list.html",
        {
            "rows": [build_click_row(click, date.today()) for click in page],
            "page_obj": page,
            "form": form,
        },
    )


def click_detail(request: HttpRequest, click_id: int) -> HttpResponse:
    """Q20: переход со ссылкой и владельцем одним SQL-запросом."""
    click = get_object_or_404(Click.objects.with_link(), pk=click_id)
    return render(
        request,
        "clicks/click_detail.html",
        {
            "row": build_click_row(click, date.today()),
        },
    )
