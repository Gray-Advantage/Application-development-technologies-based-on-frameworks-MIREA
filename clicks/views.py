"""Представления страниц переходов по коротким ссылкам."""

from django.conf import settings
from django.http import HttpRequest, HttpResponse

from homepage.views import page
from models.clicks import find_click_by_id
from storage import load_all


def clicks(request: HttpRequest) -> HttpResponse:
    """Страница /clicks/: список переходов из data/clicks.json."""
    _, _, clicks_list = load_all(settings.DATA_DIR)

    items = ""
    for click in clicks_list:
        items += f"""
        <li class="list-group-item">
            <a href="/clicks/{click.id}/">Переход №{click.id}</a>
            {click.clicked_at} — {click.link.short_url}
            <span class="badge bg-info">{click.source}</span>
        </li>
        """

    content = f"""
    <h1>Переходы</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Переходы", content))


def click_detail(request: HttpRequest, click_id: int) -> HttpResponse:
    """Страница /clicks/<int:click_id>/: карточка одного перехода."""
    _, _, clicks_list = load_all(settings.DATA_DIR)
    click = find_click_by_id(clicks_list, click_id)

    if click is None:
        content = """
        <h1 class="text-danger">Переход не найден</h1>
        <a href="/clicks/" class="btn btn-outline-secondary">
            ← к списку переходов
        </a>
        """
        return HttpResponse(
            page("Переход не найден", content),
            status=404,
        )

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Переход №{click.id}</h5>
            <p class="card-text">
                <strong>Короткая ссылка:</strong>
                <a href="/links/{click.link.code}/">
                    {click.link.short_url}
                </a>
            </p>
            <p class="card-text">
                <strong>Исходный адрес:</strong> {click.link.url}
            </p>
            <p class="card-text">
                <strong>Владелец ссылки:</strong>
                {click.link.owner.username}
            </p>
            <p class="card-text">
                <strong>Дата перехода:</strong> {click.clicked_at}
            </p>
            <p class="card-text">
                <strong>Источник:</strong>
                <span class="badge bg-info">{click.source}</span>
            </p>
            <a href="/clicks/" class="btn btn-outline-secondary">
                ← к списку переходов
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(f"Переход №{click.id}", content), status=200)
