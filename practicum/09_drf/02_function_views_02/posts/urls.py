"""
Напишите view-функцию `api_posts_detail()`, которая обрабатывает запросы GET,
PUT, PATCH и DELETE: возвращает, перезаписывает, изменяет или удаляет объект
модели **Post** по его id.

В файл *urls.py* добавьте эндпоинт `api/v1/posts/<int:pk>/`, который должен
вызывать view-функцию `api_posts_detail()`.
"""

from django.urls import path
from .views import api_posts, api_posts_detail

urlpatterns = [
    path("api/v1/posts/", api_posts),
    path("api/v1/posts/<int:pk>/", api_posts_detail),
]
