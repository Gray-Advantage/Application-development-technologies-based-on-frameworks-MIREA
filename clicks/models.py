"""Модель перехода по ссылке."""

from __future__ import annotations

from django.db import models


class ClickQuerySet(models.QuerySet):
    def with_link(self) -> ClickQuerySet:
        return self.select_related("link__owner")


class Click(models.Model):
    """История переходов со ссылкой на исходный объект."""

    link = models.ForeignKey(
        "links.Link",
        on_delete=models.PROTECT,
        related_name="clicks",
        verbose_name="Ссылка",
    )
    clicked_at = models.DateField("Дата перехода")
    source = models.CharField(
        "Источник", max_length=100, blank=True, null=True
    )

    objects = ClickQuerySet.as_manager()

    class Meta:
        verbose_name = "переход"
        verbose_name_plural = "переходы"

    def __str__(self) -> str:
        return f"Переход №{self.pk} по {self.link_id}"
