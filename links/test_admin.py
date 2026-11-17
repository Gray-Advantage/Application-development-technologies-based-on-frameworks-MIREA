"""Проверка административных страниц и статусов ссылок."""

from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from clicks.models import Click
from users.models import User

from .models import Link


class ShortenerAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.manager = get_user_model().objects.create_superuser("admin")
        cls.owner = User.objects.create(
            username="student",
            email="student@example.org",
            registered_at=date(2026, 9, 1),
        )
        cls.link = Link.objects.create(
            code="example",
            url="https://example.org/",
            owner=cls.owner,
            created_at=date(2026, 9, 1),
            expires_at=date(2026, 10, 1),
        )
        Click.objects.create(
            link=cls.link, clicked_at=date(2026, 9, 2), source="telegram"
        )

    def test_admin_search_inline_and_access(self) -> None:
        listing = reverse("admin:clicks_click_changelist")
        self.assertEqual(self.client.get(listing).status_code, 302)
        self.client.force_login(self.manager)
        self.assertContains(
            self.client.get(listing, {"q": "student"}), "telegram"
        )
        detail = reverse("admin:links_link_change", args=[self.link.pk])
        self.assertContains(self.client.get(detail), 'id="clicks-group"')
        self.assertEqual(self.link.get_absolute_url(), "/links/example/")

    def test_available_depends_on_status_and_date(self) -> None:
        day = date(2026, 9, 2)
        self.assertEqual(list(Link.objects.available_on(day)), [self.link])
        self.link.deactivate()
        self.assertEqual(self.link.status, Link.Status.DISABLED)
        self.assertFalse(Link.objects.available_on(day).exists())
        self.assertFalse(Link.objects.available_on(date(2026, 11, 1)).exists())
