"""Представления страниц коротких ссылок."""

from datetime import date

from django.conf import settings
from django.http import HttpRequest, HttpResponse

from homepage.views import page
from models.clicks import count_clicks_by, get_clicks_per_day, is_popular
from models.links import find_link_by_code
from storage import load_all


def links(request: HttpRequest) -> HttpResponse:
    """Страница /links/: список ссылок из data/links.json."""
    _, links_list, clicks_list = load_all(settings.DATA_DIR)
    counts = count_clicks_by(clicks_list, "link")
    today = date.today()

    items = ""
    for link in links_list:
        badge = "bg-success" if link.is_available(today) else "bg-secondary"
        items += f"""
        <li class="list-group-item">
            <a href="/links/{link.code}/">{link.short_url}</a>
            <span class="badge {badge}">{link.get_state(today)}</span>
            <span class="text-muted">
                переходов: {counts.get(link, 0)},
                владелец: {link.owner.username}
            </span>
        </li>
        """

    content = f"""
    <h1>Короткие ссылки</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Ссылки", content))


def link_detail(request: HttpRequest, code: str) -> HttpResponse:
    """Страница /links/<slug:code>/: карточка ссылки и её статистика."""
    _, links_list, clicks_list = load_all(settings.DATA_DIR)
    link = find_link_by_code(links_list, code)

    if link is None:
        content = """
        <h1 class="text-danger">Ссылка не найдена</h1>
        <a href="/links/" class="btn btn-outline-secondary">
            ← к списку ссылок
        </a>
        """
        return HttpResponse(
            page("Ссылка не найдена", content),
            status=404,
        )

    today = date.today()
    clicks_count = count_clicks_by(clicks_list, "link").get(link, 0)
    per_day = get_clicks_per_day(clicks_count, link.days_passed(today))
    badge = "bg-success" if link.is_available(today) else "bg-secondary"
    popular = "да" if is_popular(link, clicks_count, today) else "нет"

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{link.short_url}</h5>
            <p class="card-text">
                <strong>Исходный адрес:</strong>
                <a href="{link.url}">{link.url}</a>
            </p>
            <p class="card-text">
                <strong>Короткий код:</strong> {link.code}
            </p>
            <p class="card-text">
                <strong>Владелец:</strong> {link.owner.username}
                ({link.owner.email})
            </p>
            <p class="card-text">
                <strong>Создана:</strong> {link.created_at},
                <strong>действует до:</strong> {link.expires_at}
            </p>
            <p class="card-text">
                Состояние:
                <span class="badge {badge}">{link.get_state(today)}</span>
            </p>
            <p class="card-text">
                <strong>Переходов:</strong> {clicks_count},
                в день: {per_day:.2f}, популярна: {popular}
            </p>
            <a href="/links/" class="btn btn-outline-secondary">
                ← к списку ссылок
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(link.code, content), status=200)
