"""Интеграционные проверки ORM, переноса и пользовательских сценариев."""

from datetime import date
from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.db.models.deletion import ProtectedError
from django.test import TestCase

from links.models import Link
from links.queries import statistics
from users.models import User
from .models import Click


class ProjectTests(TestCase):
    """Тестовая Django-база из миграций, исходная SQLite только читается."""

    @classmethod
    def setUpTestData(cls) -> None:
        call_command("import_legacy", stdout=StringIO())

    def test_import_is_repeatable(self) -> None:
        call_command("import_legacy", stdout=StringIO())
        self.assertEqual(
            (
                User.objects.count(),
                Link.objects.count(),
                Click.objects.count(),
            ),
            (3, 5, 24),
        )
        click = Click.objects.select_related("link__owner").get(pk=4)
        self.assertEqual(click.link.owner.username, "anna_smirnova")

    def test_import_conflict_preserves_data(self) -> None:
        User.objects.filter(pk=2).update(username="changed")
        with self.assertRaises(CommandError):
            call_command("import_legacy", stdout=StringIO())
        self.assertEqual(User.objects.get(pk=2).username, "changed")
        self.assertEqual(Click.objects.count(), 24)

    def test_pages_and_missing_objects(self) -> None:
        for path in (
            "/",
            "/links/",
            "/links/mirea/",
            "/clicks/",
            "/clicks/1/",
            "/links/statistics/",
        ):
            self.assertEqual(self.client.get(path).status_code, 200, path)
        for path in ("/links/missing/", "/clicks/99999/"):
            self.assertEqual(self.client.get(path).status_code, 404)

    def test_availability_and_search(self) -> None:
        response = self.client.get(
            "/links/available/",
            {
                "date": "2026-09-15",
                "q": "mirea",
            },
        )
        self.assertEqual(
            {c["link"].code for c in response.context["cards"]},
            {"mirea", "5448c3"},
        )
        response = self.client.get(
            "/links/available/",
            {
                "date": "2026-09-15",
                "q": "promo",
            },
        )
        self.assertEqual(response.context["cards"], [])
        link = Link.objects.get(pk="mirea")
        self.assertFalse(link.is_available(date(2026, 10, 1)))
        self.assertFalse(link.is_available(date(2026, 8, 1)))

    def test_filters_sorting_pagination(self) -> None:
        response = self.client.get(
            "/clicks/",
            {
                "owner": "2",
                "code": "mirea",
                "sort": "-date",
                "page": "2",
            },
        )
        page = response.context["page_obj"]
        self.assertEqual(page.paginator.count, 12)
        self.assertEqual(page.number, 2)
        dates = [row["click"].clicked_at for row in response.context["rows"]]
        self.assertEqual(dates, sorted(dates, reverse=True))
        self.assertContains(response, "owner=2&amp;code=mirea&amp;sort=-date")
        response = self.client.get("/clicks/", {"page": "abc"})
        self.assertEqual(response.context["page_obj"].number, 1)
        response = self.client.get("/clicks/", {"page": "9999"})
        self.assertEqual(response.context["page_obj"].number, 5)

    def test_invalid_and_empty_filters(self) -> None:
        for params in (
            {"date": "abc"},
            {"owner": "bad"},
            {"owner": "9" * 100},
        ):
            response = self.client.get("/clicks/", params)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context["error"])
            self.assertEqual(response.context["rows"], [])
        response = self.client.get("/clicks/", {"q": "zzzz"})
        self.assertContains(response, "Переходы не найдены")
        self.assertEqual(self.client.get("/clicks/?sort=bad").status_code, 200)

    def test_statistics_and_no_click_links(self) -> None:
        original = Link.objects.get(pk="mirea")
        original.pk = "zero"
        original.save(force_insert=True)
        data = statistics()
        self.assertEqual(data["click_totals"][0]["total"], 24)
        self.assertIn({"label": "zero", "total": 0}, list(data["by_link"]))
        for value in data.values():
            list(value)  # Все запросы каталога реально выполняются.

    def test_related_objects_one_query(self) -> None:
        with self.assertNumQueries(1):
            click = Click.objects.select_related("link__owner").get(pk=1)
            self.assertEqual(click.link.owner.username, "ivan_petrov")

    def test_crud_and_protected_history(self) -> None:
        link = Link.objects.get(pk="mirea")
        with self.assertRaises(ProtectedError):
            link.delete()
        link.deactivate()
        link.refresh_from_db()
        self.assertFalse(link.is_active)
        self.assertEqual(link.clicks.count(), 12)
        call_command("demo_orm", stdout=StringIO())
        self.assertFalse(Link.objects.filter(pk="demo-pr9").exists())
