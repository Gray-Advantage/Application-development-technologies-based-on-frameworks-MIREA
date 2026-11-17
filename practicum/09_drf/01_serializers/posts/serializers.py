"""
Создайте сериализатор для модели **Post** в проекте Yatube.

Импортируйте фреймворк `rest_framework.serializers` и на основе класса
`serializers.ModelSerializer` создайте класс `PostSerializer`.

В `PostSerializer` опишите `class Meta` с двумя полями: `fields` и `model`.

В `fields` перечислите поля для вывода текста, автора и даты публикации.
Сериализатор не должен обрабатывать поле id из модели **Post**.

В поле `model` укажите модель, с которой будет связан сериализатор.
"""

from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("text", "author", "pub_date")
        model = Post
