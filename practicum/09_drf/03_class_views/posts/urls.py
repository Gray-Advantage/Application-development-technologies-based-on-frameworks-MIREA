"""
Напишите view-класс `APIPost()`, унаследовав его от APIView.

Он будет работать с queryset, содержащим все объекты модели **Post**. При
POST-запросе этот класс должен создавать новый объект модели **Post** и
возвращать его, а по GET-запросу должен возвращаться сериализованный список
всех объектов модели **Post**.
"""

from django.urls import path

from .views import APIPost

urlpatterns = [
    path("api/v1/posts/", APIPost.as_view()),
]
