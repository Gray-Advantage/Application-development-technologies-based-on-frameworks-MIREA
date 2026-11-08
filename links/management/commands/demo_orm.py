"""Воспроизводимая демонстрация CRUD с откатом тестовых изменений."""

from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction

from clicks.models import Click
from links.models import Link
from users.models import User


class Command(BaseCommand):
    help = "Показать CRUD в транзакции с обязательным откатом"

    @transaction.atomic
    def handle(self, *args, **options) -> None:
        user = User.objects.create(
            username="demo-pr9",
            email="demo-pr9@example.com",
            registered_at=date.today(),
        )
        link = Link.objects.create(
            code="demo-pr9",
            url="https://example.com",
            owner=user,
            created_at=date.today(),
            expires_at=date.today() + timedelta(days=30),
        )
        click = Click.objects.create(link=link, clicked_at=date.today())
        self.stdout.write(str(Link.objects.get(pk=link.pk)))
        link.deactivate()
        link.refresh_from_db()
        self.stdout.write(f"После save(): is_active={link.is_active}")
        self.stdout.write(f"Обратная связь: {link.clicks.count()}")
        click.delete()
        link.delete()
        user.delete()
        self.stdout.write("Тестовые объекты удалены; транзакция откатывается.")
        transaction.set_rollback(True)
