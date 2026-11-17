"""Модель короткой ссылки."""

from __future__ import annotations

from datetime import date

from django.db import models
from django.urls import reverse


class LinkQuerySet(models.QuerySet):
    def enabled(self) -> LinkQuerySet:
        return self.filter(status=Link.Status.ENABLED)

    def available_on(self, day: date) -> LinkQuerySet:
        return self.enabled().filter(created_at__lte=day, expires_at__gt=day)


class Link(models.Model):
    """Ссылка с владельцем и сроком действия."""

    class Status(models.TextChoices):
        ENABLED = "enabled", "Включена"
        DISABLED = "disabled", "Отключена"

    code = models.SlugField("Короткий код", max_length=30, primary_key=True)
    url = models.URLField("Исходный URL", max_length=2048)
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="links",
        verbose_name="Владелец",
    )
    created_at = models.DateField("Дата создания")
    expires_at = models.DateField(
        "Действует до", help_text="В указанную дату ссылка уже недоступна."
    )
    status = models.CharField(
        "Статус", max_length=8, choices=Status.choices, default=Status.ENABLED
    )

    objects = LinkQuerySet.as_manager()

    class Meta:
        verbose_name = "короткая ссылка"
        verbose_name_plural = "короткие ссылки"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(expires_at__gt=models.F("created_at")),
                name="link_positive_lifetime",
            )
        ]

    def get_absolute_url(self) -> str:
        return reverse("links:detail", kwargs={"code": self.code})

    @property
    def is_active(self) -> bool:
        return self.status == self.Status.ENABLED

    @property
    def short_url(self) -> str:
        return "https://sl.mirea/" + self.code

    def days_left(self, today: date) -> int:
        return (self.expires_at - today).days

    def days_passed(self, today: date) -> int:
        return (today - self.created_at).days

    def is_available(self, today: date) -> bool:
        return self.is_active and self.created_at <= today < self.expires_at

    def get_state(self, today: date) -> str:
        if not self.is_active:
            return "отключена"
        if today < self.created_at:
            return "ещё не создана"
        if self.days_left(today) <= 0:
            return "истекла"
        return "скоро истекает" if self.days_left(today) <= 7 else "активна"

    def deactivate(self) -> None:
        """Отключить и сохранить ссылку, оставив историю переходов."""
        self.status = self.Status.DISABLED
        self.save(update_fields=["status"])

    def __str__(self) -> str:
        return self.short_url
