"""
Запретите любые запросы к публикациям в обеденное время (с 13:00 до 14:00).
Опишите в приложении **api** тротлинг-класс `LunchBreakThrottle` и подключите
его к соответствующему view-классу публикаций.

![](https://pictures.s3.yandex.net:443/resources/image_1708513946.png)
"""

from rest_framework import generics, permissions
from rest_framework.settings import api_settings

from posts.models import Post

from .permissions import IsAuthorOrReadOnlyPermission
from .serializers import PostSerializer
from .throttling import LunchBreakThrottle


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    throttle_classes = (
        *api_settings.DEFAULT_THROTTLE_CLASSES,
        LunchBreakThrottle,
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    throttle_classes = (
        *api_settings.DEFAULT_THROTTLE_CLASSES,
        LunchBreakThrottle,
    )
