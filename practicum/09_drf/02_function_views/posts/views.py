"""
Опишите view-функцию API `api_posts()`, которая будет работать с объектами
модели **Post** и обрабатывать только GET- и POST-запросы:

- в ответ на GET-запрос функция должна возвращать queryset со всеми объектами
модели **Post**;
- при POST-запросе функция должна создавать новый объект и возвращать его.

В файл *urls.py* добавьте эндпоинт `api/v1/posts/`, который вызывает
view-функцию API `api_posts`.

Заранее предусмотрите возможность дальнейшего развития проекта: версионируйте
API. Начните с первой версии: эндпоинты API должны выглядеть так:
`api/v1/...`.

В файле *serializers.py* подготовлен сериализатор `PostSerializer`.
"""

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer


@api_view(["GET", "POST"])
def api_posts(request):
    if request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
