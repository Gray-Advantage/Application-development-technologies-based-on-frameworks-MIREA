"""Каркас страниц проекта, главная страница и обработчик ошибки 404."""

from django.http import HttpRequest, HttpResponse

BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
    "/dist/css/bootstrap.min.css"
)


def page(title: str, content: str) -> str:
    """Собрать HTML-документ: кодировку, Bootstrap и навигацию.

    Общий каркас всех страниц проекта: конкретные представления
    передают только заголовок вкладки и содержимое страницы.
    """
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{BOOTSTRAP_CSS}">
</head>
<body>
    <nav class="nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/links/">Ссылки</a>
        <a class="nav-link" href="/clicks/">Переходы</a>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница: описание сервиса и переходы в разделы."""
    content = """
    <h1 class="display-4">Сервис сокращения ссылок</h1>
    <p class="lead">
        Короткие ссылки, срок их действия и статистика переходов.
    </p>
    <p>Основные разделы:</p>
    <a href="/links/" class="btn btn-primary me-2">Ссылки</a>
    <a href="/clicks/" class="btn btn-secondary">Переходы</a>
    """
    return HttpResponse(page("Сервис сокращения ссылок", content))


def page_not_found(
    request: HttpRequest, exception: Exception
) -> HttpResponse:
    """Собственная страница ошибки 404 для всех приложений проекта."""
    content = """
    <h1 class="text-danger">404 – страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 – страница не найдена", content),
        status=404,
    )
