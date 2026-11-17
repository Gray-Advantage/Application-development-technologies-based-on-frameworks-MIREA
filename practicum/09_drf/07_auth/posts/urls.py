"""
Добавьте в проект Yatube API механизм аутентификации при помощи обычного
токена, реализованный на view-функциях.

Сделайте так, чтобы при создании нового поста через POST-запрос в поле *author*
автоматически записывался объект автора по токену.

Вам нужно:

- Сделать доступ к API только после авторизации; опишите эндпоинт
*api/v1/api-token-auth/*, по которому можно будет получать токен.
- В сериализаторе настроить поле `author` в режим «только для чтения».
- При создании публикации в поле «автор» указать пользователя, полученного из
объекта `request.user`.
- Описать обработчик GET-запроса для получения поста в функции
`**api_posts_detail`.
- Разрешить изменение или удаление постов только авторам этих постов, в
противном случае возвращать статус 403.
"""

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import api_posts, api_posts_detail

urlpatterns = [
    path("api/v1/posts/", api_posts),
    path("api/v1/posts/<int:pk>/", api_posts_detail),
    path("api/v1/api-token-auth/", obtain_auth_token),
]
