"""Используемые ORM-выражения Q01–Q17 для защиты ПР9."""

from datetime import date

from django.db.models import Count, F, Min, Max, Q
from django.db.models.query import QuerySet

from clicks.models import Click
from users.models import User
from .models import Link


def link_list() -> QuerySet:
    """Q01: список, связь и число переходов без N+1."""
    return (
        Link.objects.select_related("owner")
        .annotate(clicks_count=Count("clicks"))
        .order_by("created_at", "code")
    )


def available_links(day: date, query: str) -> QuerySet:
    """Q02: несколько условий и поиск по двум полям."""
    return (
        link_list()
        .filter(is_active=True, created_at__lte=day, expires_at__gt=day)
        .filter(Q(code__icontains=query) | Q(url__icontains=query))
    )


def click_list(params: dict) -> QuerySet:
    """Q03: фильтры, поиск по связям и безопасная сортировка."""
    result = Click.objects.select_related("link__owner")
    if params.get("date"):
        result = result.filter(clicked_at=params["date"])
    if params.get("owner"):
        result = result.filter(link__owner_id=params["owner"])
    if params.get("code"):
        result = result.filter(link_id=params["code"])
    if params.get("q"):
        result = result.filter(
            Q(source__icontains=params["q"])
            | Q(link__url__icontains=params["q"])
            | Q(link__owner__username__icontains=params["q"])
        )
    if params.get("active") == "1":
        result = result.exclude(link__is_active=False)
    fields = {
        "date": "clicked_at",
        "-date": "-clicked_at",
        "code": "link_id",
        "owner": "link__owner__username",
    }
    return result.order_by(
        fields.get(params.get("sort", "date"), "clicked_at"), "id"
    )


def statistics() -> dict:
    """Q04–Q17 — самостоятельные используемые выборки и сводки."""
    return {
        # Q04: условная сводная агрегация.
        "totals": [
            Link.objects.aggregate(
                total=Count("pk"), active=Count("pk", filter=Q(is_active=True))
            )
        ],
        # Q05: агрегаты дат.
        "click_totals": [
            Click.objects.aggregate(
                total=Count("pk"),
                first_date=Min("clicked_at"),
                last_date=Max("clicked_at"),
            )
        ],
        # Q06: LEFT JOIN сохраняет ссылки без переходов.
        "by_link": Link.objects.values(label=F("code"))
        .annotate(total=Count("clicks"))
        .order_by("-total", "label"),
        # Q07: группировка источников.
        "by_source": Click.objects.values(label=F("source"))
        .annotate(total=Count("pk"))
        .order_by("-total", "label"),
        # Q08: HAVING по числу переходов.
        "popular": Link.objects.values(label=F("code"))
        .annotate(total=Count("clicks"))
        .filter(total__gte=3)
        .order_by("-total", "label"),
        # Q09: обратная связь и сортировка по одному полю.
        "by_owner": User.objects.values(label=F("username"))
        .annotate(total=Count("links"))
        .order_by("label"),
        # Q10: срез и values.
        "recent": Click.objects.order_by("-clicked_at", "-id").values(
            "id", "clicked_at"
        )[:5],
        # Q11: DISTINCT.
        "sources": Click.objects.order_by("source")
        .values("source")
        .distinct(),
        # Q12: один фильтр.
        "disabled": Link.objects.filter(is_active=False).order_by("code"),
        # Q13: исключение истёкших.
        "unexpired": Link.objects.exclude(
            expires_at__lte=date.today()
        ).order_by("code"),
        # Q14: поиск по одному строковому полю.
        "telegram": Click.objects.filter(source__icontains="telegram"),
        # Q15: отдельная фильтрация по связанному полю.
        "education": Click.objects.filter(link__url__icontains="mirea.ru"),
        # Q16: получение всего набора владельцев.
        "owners": User.objects.all().order_by("username"),
        # Q17: F и values, без лишнего select_related для словарей.
        "click_labels": Click.objects.annotate(
            code=F("link__code"), owner=F("link__owner__username")
        )
        .values("id", "code", "owner")
        .order_by("id")[:5],
    }
