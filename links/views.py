"""Страницы ссылок через Django ORM."""

from datetime import date

from django.contrib.auth.decorators import login_required, permission_required
from django.db import IntegrityError, transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST

from models.clicks import POPULAR_CLICKS, get_clicks_per_day
from .forms import AvailabilityForm, LinkForm
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
    form = AvailabilityForm(
        request.GET or None, initial={"date": date.today()}
    )
    cards = []
    if not form.is_bound or form.is_valid():
        day = form.cleaned_data.get("date") if form.is_bound else None
        day = day or date.today()
        query = form.cleaned_data.get("q", "") if form.is_bound else ""
        cards = [
            build_link_card(link, day) for link in available_links(day, query)
        ]
    return render(
        request,
        "links/available.html",
        {"cards": cards, "form": form},
    )


@login_required(login_url="admin:login")
@permission_required("links.add_link", raise_exception=True)
@require_http_methods(["GET", "HEAD", "POST"])
def link_create(request: HttpRequest) -> HttpResponse:
    form = (
        LinkForm(request.POST, request.FILES)
        if request.method == "POST"
        else LinkForm()
    )
    if form.is_valid():
        link = form.save(commit=False)
        try:
            with transaction.atomic():
                link.save(force_insert=True)
        except IntegrityError:
            if not Link.objects.filter(pk=link.pk).exists():
                raise
            if link.preview:
                link.preview.delete(save=False)
            form.add_error("code", "Ссылка с таким кодом уже существует.")
        else:
            return redirect(link)
    return render(
        request,
        "links/link_form.html",
        {
            "form": form,
            "title": "Создать ссылку",
            "cancel_url": reverse("links:list"),
        },
    )


@login_required(login_url="admin:login")
@permission_required("links.change_link", raise_exception=True)
@require_http_methods(["GET", "HEAD", "POST"])
def link_edit(request: HttpRequest, code: str) -> HttpResponse:
    link = get_object_or_404(Link.objects.enabled(), pk=code)
    form = (
        LinkForm(request.POST, request.FILES, instance=link)
        if request.method == "POST"
        else LinkForm(instance=link)
    )
    if form.is_valid():
        link = form.save(commit=False)
        link.save(update_fields=["url", "expires_at", "preview"])
        return redirect(link)
    return render(
        request,
        "links/link_form.html",
        {
            "form": form,
            "title": "Редактировать ссылку",
            "cancel_url": link.get_absolute_url(),
        },
    )


@require_POST
@login_required(login_url="admin:login")
@permission_required("links.change_link", raise_exception=True)
def link_disable(request: HttpRequest, code: str) -> HttpResponse:
    link = get_object_or_404(Link.objects.enabled(), pk=code)
    link.deactivate()
    return redirect(link)


def stats(request: HttpRequest) -> HttpResponse:
    """Q04–Q17: сводки и связанные данные."""
    return render(request, "links/statistics.html", statistics())
