"""Подключение SQLite с проверкой внешних ключей и именованными полями."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from collections.abc import Iterator

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "shortener.sqlite"


@contextmanager
def connect(path: Path = DATABASE_PATH) -> Iterator[sqlite3.Connection]:
    """Открыть соединение; подтвердить транзакцию и обязательно закрыть."""
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def create_schema(path: Path = DATABASE_PATH) -> None:
    """Создать отсутствующие таблицы, сохранив существующие данные."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with connect(path) as connection:
        connection.executescript(
            (BASE_DIR / "sql" / "schema.sql").read_text(encoding="utf-8")
        )
