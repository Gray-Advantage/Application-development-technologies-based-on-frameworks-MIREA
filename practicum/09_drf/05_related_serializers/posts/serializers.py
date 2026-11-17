"""
Настройте API для Yatube так, чтобы при запросе постов возвращалась информация
о группе, в которой опубликован пост. Данные о группе должны возвращаться в
виде значения её поля `slug`.

Добавьте возможность при создании или изменении поста через API опционально
указывать группу, передавая в теле запроса поле `slug`.

Для решения задачи вам нужно дописать несколько строк в классе
`PostSerializer`.
"""

from rest_framework import serializers

from .models import Post, Group


class PostSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(
        slug_field="slug", queryset=Group.objects.all(), required=False
    )

    class Meta:
        fields = ("id", "text", "author", "image", "pub_date", "group")
        model = Post
