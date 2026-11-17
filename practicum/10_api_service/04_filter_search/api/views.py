"""
При публикации одной из своих дневниковых записей пользователь *@leo* по ошибке
вставил в текст поста свой почтовый индекс. В какой именно пост попала эта
информация — он не помнит, но очень хочет удалить её из текста.

Помогите пользователю решить эту проблему и найти нужный пост через API.
Почтовые индексы России состоят из 6 цифр. Такую последовательность в тексте
легко обнаружить при помощи регулярного выражения.

Настройте поиск по текстам публикаций так, чтобы в качестве поисковых запросов
можно было использовать регулярные выражения.
"""

from rest_framework import filters, generics, permissions

from posts.models import Post

from .permissions import IsAuthorOrReadOnlyPermission
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("$text",)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
