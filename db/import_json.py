"""Перенос JSON в SQLite: python -m db.import_json.

Повторный запуск не меняет существующие записи; ошибка откатывает весь импорт.
"""

import json
from pathlib import Path

from .database import BASE_DIR, DATABASE_PATH, connect, create_schema


def import_json(
    data_dir: Path = BASE_DIR / "data", path: Path = DATABASE_PATH
) -> dict[str, int]:
    """Импортировать родителей перед дочерними записями в одной транзакции."""
    records = {
        name: json.loads((data_dir / f"{name}.json").read_text("utf-8"))
        for name in ("users", "links", "clicks")
    }
    create_schema(path)
    with connect(path) as connection:
        connection.executemany(
            "INSERT INTO users VALUES (:id,:username,:email,:registered_at) "
            "ON CONFLICT(id) DO NOTHING",
            records["users"],
        )
        connection.executemany(
            "INSERT INTO links VALUES "
            "(:code,:url,:owner_id,:created_at,:expires_at,:is_active) "
            "ON CONFLICT(code) DO NOTHING",
            records["links"],
        )
        connection.executemany(
            "INSERT INTO clicks VALUES (:id,:code,:clicked_at,:source) "
            "ON CONFLICT(id) DO NOTHING",
            records["clicks"],
        )
        connection.commit()
        return {
            name: connection.execute(query).fetchone()[0]
            for name, query in {
                "users": "SELECT COUNT(*) FROM users",
                "links": "SELECT COUNT(*) FROM links",
                "clicks": "SELECT COUNT(*) FROM clicks",
            }.items()
        }


if __name__ == "__main__":
    print(import_json())
