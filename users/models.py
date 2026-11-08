"""Пользователи предметной области, отдельно от Django auth."""

from django.db import models


class User(models.Model):
    """Владелец коротких ссылок."""

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    registered_at = models.DateField()

    def __str__(self) -> str:
        return self.username
