"""Модель короткой ссылки."""

from datetime import date

from django.db import models


class Link(models.Model):
    """Ссылка с владельцем и сроком действия."""

    code = models.SlugField(max_length=30, primary_key=True)
    url = models.URLField(max_length=2048)
    owner = models.ForeignKey(
        "users.User", on_delete=models.PROTECT, related_name="links"
    )
    created_at = models.DateField()
    expires_at = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(expires_at__gt=models.F("created_at")),
                name="link_positive_lifetime",
            )
        ]

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
        self.is_active = False
        self.save(update_fields=["is_active"])

    def __str__(self) -> str:
        return self.short_url
