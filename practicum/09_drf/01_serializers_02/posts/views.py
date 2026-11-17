"""
Сериализатор готов, самое время проверить его в работе — отправить запрос и в
ответ получить JSON. Но для этого необходимо описать маршрут и дописать
view-функцию.

При GET-запросе по адресу `api/v1/posts/` должна вызываться view-функция
`get_post()`. В качестве параметра view-функция должна ожидать переменную `pk`
с целочисленным значением. В ответ функция должна возвращать объект публикации
по его id.

View-функция `get_post()` должна возвращать объект **JsonResponse**. Для этого
импортируйте класс JsonResponse из модуля `django.http` и передайте в
конструктор класса **JsonResponse** данные из сериализатора.
"""

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Post
from .serializers import PostSerializer


def get_post(request, pk):
    if request.method == "GET":
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)
