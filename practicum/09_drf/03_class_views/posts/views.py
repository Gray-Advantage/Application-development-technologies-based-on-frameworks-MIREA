"""
Напишите view-класс `APIPost()`, унаследовав его от APIView.

Он будет работать с queryset, содержащим все объекты модели **Post**. При
POST-запросе этот класс должен создавать новый объект модели **Post** и
возвращать его, а по GET-запросу должен возвращаться сериализованный список
всех объектов модели **Post**.
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .serializers import PostSerializer


class APIPost(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
