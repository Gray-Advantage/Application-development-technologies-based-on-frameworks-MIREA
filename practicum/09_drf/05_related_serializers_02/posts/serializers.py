"""
Добавьте к постам хештеги. Хештеги должны храниться в отдельной таблице в БД и
быть связаны с постами отношением «многие-ко-многим».

При запросе постов должна возвращаться информация о всех связанных с конкретным
постом хештегах, а при добавлении или обновлении поста нужно обеспечить
возможность передавать названия хештегов списком прямо в теле запроса. Без
указания хештегов пост через API тоже должен создаваться.

Пример POST-запроса для создания поста с хештегами:

```python
{
    "text": "Текст для моего поста",
    "author": 1,
    "tag": [
        {"name": "хобби"},
        {"name": "личное"}
        ]
}
```
"""

from rest_framework import serializers

from .models import Group, Post, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name",)
        model = Tag


class PostSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(
        slug_field="slug", queryset=Group.objects.all(), required=False
    )
    tag = TagSerializer(many=True, required=False)

    class Meta:
        fields = ("id", "text", "author", "image", "pub_date", "group", "tag")
        model = Post

    def create(self, validated_data):
        tags_data = validated_data.pop("tag", [])
        post = Post.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            post.tag.add(tag)
        return post

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tag", None)
        post = super().update(instance, validated_data)
        if tags_data is not None:
            tags = [
                Tag.objects.get_or_create(**tag_data)[0]
                for tag_data in tags_data
            ]
            post.tag.set(tags)
        return post
