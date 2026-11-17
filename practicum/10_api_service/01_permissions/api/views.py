"""
В тренажёр загружена облегчённая версия проекта Yatube; она реализована на
дженериках.

Настройте права доступа так, чтобы неаутентифицированные пользователи могли
только читать публикации; все остальные операции должны быть доступны только
пользователям с действующим токеном.
"""

from rest_framework import generics, permissions

from posts.models import Post

from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
