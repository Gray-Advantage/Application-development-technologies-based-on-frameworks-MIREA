"""Сценарии создания, редактирования и отключения ссылки."""

from datetime import date, timedelta
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings

from users.models import User

from .models import Link


class LinkFormTests(TestCase):
    create_url = "/links/manage/create/"

    @classmethod
    def setUpTestData(cls) -> None:
        accounts = get_user_model()
        cls.editor = accounts.objects.create_superuser("editor")
        cls.reader = accounts.objects.create_user("reader", is_staff=True)
        cls.owner = User.objects.create(
            username="owner",
            email="owner@example.org",
            registered_at=date.today(),
        )

    def payload(self, **overrides: str) -> dict:
        return {
            "code": "form-demo",
            "owner": str(self.owner.pk),
            "url": "https://example.org/initial",
            "expires_at": (date.today() + timedelta(days=10)).isoformat(),
            **overrides,
        }

    def test_crud_keeps_slug_and_applies_post_only_disable(self) -> None:
        self.client.force_login(self.editor)
        self.assertContains(self.client.get(self.create_url), "Короткий код")
        self.assertRedirects(
            self.client.post(self.create_url, self.payload()),
            "/links/form-demo/",
        )
        self.assertRedirects(
            self.client.post(
                "/links/form-demo/edit/",
                self.payload(
                    url="https://example.org/changed", code="changed"
                ),
            ),
            "/links/form-demo/",
        )
        link = Link.objects.get(pk="form-demo")
        self.assertEqual(link.url, "https://example.org/changed")
        self.assertEqual(link.owner, self.owner)
        disable_url = "/links/form-demo/disable/"
        self.assertEqual(self.client.get(disable_url).status_code, 405)
        self.assertRedirects(
            self.client.post(disable_url), link.get_absolute_url()
        )
        link.refresh_from_db()
        self.assertFalse(link.is_active)
        self.assertEqual(
            self.client.get("/links/unknown/edit/").status_code, 404
        )

    def test_invalid_input_and_duplicate_do_not_save(self) -> None:
        self.client.force_login(self.editor)
        for payload in (
            self.payload(expires_at=date.today().isoformat()),
            self.payload(code="statistics"),
            self.payload(url="javascript:alert(1)"),
            self.payload(owner=""),
        ):
            response = self.client.post(self.create_url, payload)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context["form"].errors)
        self.assertFalse(Link.objects.exists())
        self.client.post(self.create_url, self.payload())
        response = self.client.post(
            self.create_url, self.payload(url="https://example.org/duplicate")
        )
        self.assertIn("code", response.context["form"].errors)
        self.assertEqual(Link.objects.get().url, "https://example.org/initial")

    def test_permission_and_csrf(self) -> None:
        self.assertEqual(self.client.get(self.create_url).status_code, 302)
        self.client.force_login(self.reader)
        self.assertEqual(
            self.client.post(self.create_url, self.payload()).status_code, 403
        )
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.editor)
        self.assertEqual(
            csrf_client.post(self.create_url, self.payload()).status_code, 403
        )
        self.assertFalse(Link.objects.exists())

    def test_upload_validates_image_and_serves_preview(self) -> None:
        from io import BytesIO
        from PIL import Image

        self.client.force_login(self.editor)
        with TemporaryDirectory() as directory, override_settings(
            MEDIA_ROOT=directory
        ):
            upload = SimpleUploadedFile(
                "fake.png", b"text", content_type="image/png"
            )
            response = self.client.post(
                self.create_url, {**self.payload(), "preview": upload}
            )
            self.assertIn("preview", response.context["form"].errors)
            self.assertFalse(Link.objects.exists())
            image = BytesIO()
            Image.new("RGB", (4, 4), "red").save(image, "PNG")
            upload = SimpleUploadedFile(
                "preview.png", image.getvalue(), content_type="image/png"
            )
            self.assertRedirects(
                self.client.post(
                    self.create_url, {**self.payload(), "preview": upload}
                ),
                "/links/form-demo/",
            )
            preview = Link.objects.get().preview
            self.assertTrue(preview.storage.exists(preview.name))
            self.assertContains(
                self.client.get("/links/form-demo/"), preview.url
            )
