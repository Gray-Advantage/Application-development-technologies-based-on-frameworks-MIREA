"""
В Yatube API информация о дате создания поста передаётся по ключу `pub_date`.
Добавьте в запросы информативности: сделайте так, чтобы пользователи API
получали дату публикации поста в поле с именем `publication_date`.
"""

from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    character_quantity = serializers.SerializerMethodField()
    publication_date = serializers.DateTimeField(
        source="pub_date", read_only=True
    )

    class Meta:
        fields = (
            "id",
            "text",
            "author",
            "image",
            "character_quantity",
            "publication_date",
        )
        model = Post

    def get_character_quantity(self, obj):
        return len(obj.text)
