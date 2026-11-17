"""
Напишите на основе дженериков два view-класса: `APIPostList` и `APIPostDetail`.

Опишите два эндпоинта:

- `api/v1/posts/`,
- `api/v1/posts/<pk>/`.

Через эти эндпоинты должны быть доступны любые операции с моделью **Post**:

- POST-запрос на `api/v1/posts/` создаст новую запись.
- Запросы PUT, PATCH или DELETE к адресу `api/v1/posts/<pk>/` удалят или
изменят существующую запись.
- GET-запрос на те же адреса вернёт список объектов или один объект.
"""

from django.urls import path

from .views import APIPostList, APIPostDetail

urlpatterns = [
    path("api/v1/posts/", APIPostList.as_view()),
    path("api/v1/posts/<int:pk>/", APIPostDetail.as_view()),
]
