"""Модель перехода по ссылке."""

from django.db import models


class Click(models.Model):
    """История переходов со ссылкой на исходный объект."""

    link = models.ForeignKey(
        "links.Link", on_delete=models.PROTECT, related_name="clicks"
    )
    clicked_at = models.DateField()
    source = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return f"Переход №{self.pk} по {self.link_id}"
