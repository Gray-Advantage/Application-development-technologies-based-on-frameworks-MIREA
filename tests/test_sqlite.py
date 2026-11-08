"""Проверки переноса, целостности и исполняемого каталога запросов ПР7."""

import sqlite3
from pathlib import Path

import pytest

from db.database import BASE_DIR, connect
from db.import_json import import_json
from db.repository import queries


def test_import_and_queries(tmp_path: Path) -> None:
    """Повторный импорт не дублирует данные; все запросы исполняются."""
    path = tmp_path / "test.sqlite"
    expected = {"users": 3, "links": 5, "clicks": 24}
    assert import_json(BASE_DIR / "data", path) == expected
    assert import_json(BASE_DIR / "data", path) == expected
    with connect(path) as connection:
        for query in queries().values():
            connection.execute(
                query,
                {
                    "date": "2026-09-15",
                    "query": "%mirea%",
                    "minimum": 3,
                    "limit": 5,
                    "offset": 0,
                },
            ).fetchall()
        assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                "INSERT INTO clicks VALUES (99, ?, ?, ?)",
                ("missing", "2026-09-01", None),
            )


def test_import_rolls_back(tmp_path: Path) -> None:
    """Сбой дочерней записи откатывает импорт родителей."""
    import json

    source = tmp_path / "json"
    source.mkdir()
    for name in ("users", "links", "clicks"):
        records = json.loads((BASE_DIR / f"data/{name}.json").read_text())
        if name == "clicks":
            records[0]["code"] = "missing"
        (source / f"{name}.json").write_text(json.dumps(records))
    path = tmp_path / "bad.sqlite"
    with pytest.raises(sqlite3.IntegrityError):
        import_json(source, path)
    with connect(path) as connection:
        assert (
            connection.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0
        )
