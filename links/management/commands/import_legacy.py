"""Команда переноса исходной базы ПР7 в ORM."""

import sqlite3
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from clicks.models import Click
from db.database import DATABASE_PATH
from links.models import Link
from users.models import User


class Command(BaseCommand):
    help = "Перенести SQLite ПР7 в ORM, сохранив ключи и связи"

    def add_arguments(self, parser) -> None:
        parser.add_argument("--source", type=Path, default=DATABASE_PATH)

    def handle(self, *args, **options) -> None:
        source = options["source"].resolve()
        if not source.is_file():
            raise CommandError("Исходная база не найдена; выполните ПР7.")
        connection = sqlite3.connect(f"{source.as_uri()}?mode=ro", uri=True)
        connection.row_factory = sqlite3.Row
        try:
            records = {
                "users": connection.execute("SELECT * FROM users").fetchall(),
                "links": connection.execute("SELECT * FROM links").fetchall(),
                "clicks": connection.execute(
                    "SELECT * FROM clicks"
                ).fetchall(),
            }
            backup = source.with_name(source.stem + "_backup.sqlite")
            if not backup.exists():
                target = sqlite3.connect(backup)
                try:
                    connection.backup(target)
                finally:
                    target.close()
            with transaction.atomic():
                for row in records["users"]:
                    self.copy(
                        User,
                        {"pk": row["id"]},
                        {
                            "username": row["username"],
                            "email": row["email"],
                            "registered_at": row["registered_at"],
                        },
                    )
                for row in records["links"]:
                    self.copy(
                        Link,
                        {"pk": row["code"]},
                        {
                            "url": row["url"],
                            "owner_id": row["owner_id"],
                            "created_at": row["created_at"],
                            "expires_at": row["expires_at"],
                            "status": (
                                Link.Status.ENABLED
                                if row["is_active"]
                                else Link.Status.DISABLED
                            ),
                        },
                    )
                for row in records["clicks"]:
                    self.copy(
                        Click,
                        {"pk": row["id"]},
                        {
                            "link_id": row["code"],
                            "clicked_at": row["clicked_at"],
                            "source": row["source"],
                        },
                    )
        finally:
            connection.close()
        self.stdout.write(
            self.style.SUCCESS(
                f"Перенесено: {len(records['users'])} пользователей, "
                f"{len(records['links'])} ссылок, "
                f"{len(records['clicks'])} переходов."
            )
        )

    @staticmethod
    def copy(model, lookup: dict, values: dict) -> None:
        """Повторный запуск не дублирует записи и не затирает конфликты."""
        obj, created = model.objects.get_or_create(**lookup, defaults=values)
        if not created:
            for key, value in values.items():
                if str(getattr(obj, key)) != str(value):
                    raise CommandError(
                        f"Конфликт {model.__name__} {obj.pk}: поле {key}. "
                        "Импорт отменён без перезаписи."
                    )
