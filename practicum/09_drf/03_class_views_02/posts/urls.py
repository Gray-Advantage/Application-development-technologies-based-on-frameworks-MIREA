"""
Опишите код класса `APIPostDetail()`, наследующегося от `APIView`.

Этот класс должен обрабатывать запросы GET, PUT, PATCH и DELETE: возвращать,
изменять или удалять отдельный объект модели **Post**.

В файл *urls.py* добавьте эндпоинт `api/v1/posts/<int:pk>/`, который будет
вызывать view-класс `APIPostDetail()`.
"""

from django.urls import path
from .views import APIPost, APIPostDetail

urlpatterns = [
    path("api/v1/posts/", APIPost.as_view()),
    path("api/v1/posts/<int:pk>/", APIPostDetail.as_view()),
]
