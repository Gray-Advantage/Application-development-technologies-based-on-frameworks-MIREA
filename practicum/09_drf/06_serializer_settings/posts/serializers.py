"""
Владельцы интернет-ресурсов покупают готовые статьи на биржах; стоимость
зависит от количества символов в тексте. Настройте Yatube API так, чтобы в
ответ на GET-запрос поста (или списка постов) вместе с информацией о посте
возвращалось дополнительное поле `character_quantity`. В этом поле верните
количество символов в запрошенных публикациях.
"""

from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    character_quantity = serializers.SerializerMethodField()

    class Meta:
        fields = (
            "id",
            "text",
            "author",
            "image",
            "pub_date",
            "character_quantity",
        )
        model = Post

    def get_character_quantity(self, obj):
        return len(obj.text)
