"""Пользователи предметной области, отдельно от Django auth."""

from django.db import models


class User(models.Model):
    """Владелец коротких ссылок."""

    username = models.CharField(
        "Имя пользователя", max_length=150, unique=True
    )
    email = models.EmailField("Электронная почта", unique=True)
    registered_at = models.DateField("Дата регистрации")

    class Meta:
        verbose_name = "владелец"
        verbose_name_plural = "владельцы"

    def __str__(self) -> str:
        return self.username
