"""
Напишите view-класс `PostViewSet()`, унаследовавшись от `ModelViewSet`, и
создайте роутер для него.

Созданный роутер должен генерировать два эндпоинта:

- `api/v1/posts/`,
- `api/v1/posts/<int:pk>/`.

Через эти эндпоинты должны быть доступны любые операции с моделью Post:

- POST-запрос на `api/v1/posts/` создаст новую запись.
- Запросы PUT, PATCH или DELETE к адресу `api/v1/posts/<pk>/` изменят или
удалят существующую запись.
- GET-запрос на те же адреса вернёт список объектов или один объект.
"""

from rest_framework import viewsets

from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
