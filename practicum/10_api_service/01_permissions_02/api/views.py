"""
В приложении **api** опишите и примените пермишен, который не даст пользователю
удалить или отредактировать чужие публикации.

Запрашивать список всех публикаций или отдельную публикацию может любой
пользователь. Создавать новую публикацию может только аутентифицированный
пользователь.
"""

from rest_framework import generics, permissions

from posts.models import Post

from .permissions import IsAuthorOrReadOnlyPermission
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
    permission_classes = (IsAuthorOrReadOnlyPermission,)
