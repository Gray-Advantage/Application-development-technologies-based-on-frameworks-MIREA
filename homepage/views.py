"""Представления главной страницы и обработчик ошибки 404."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница: описание сервиса и переходы в разделы."""
    return render(request, "homepage/index.html")


def page_not_found(
    request: HttpRequest, exception: Exception
) -> HttpResponse:
    """Собственная страница ошибки 404 для всех приложений проекта."""
    return render(request, "homepage/not_found.html", status=404)
