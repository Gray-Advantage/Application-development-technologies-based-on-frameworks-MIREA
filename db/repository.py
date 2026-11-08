"""SQL-запросы и восстановление объектов для существующих шаблонов ПР6."""

from datetime import date

from models import Click, Link, User
from .database import BASE_DIR, DATABASE_PATH, connect


def queries() -> dict[str, str]:
    """Читать единый исполняемый каталог SQL, используемый веб-приложением."""
    sections = (
        (BASE_DIR / "sql/queries.sql")
        .read_text("utf-8")
        .split("-- name: ")[1:]
    )
    return {
        part.splitlines()[0]: "\n".join(part.splitlines()[1:])
        for part in sections
    }


def select(name: str, params: dict | None = None) -> list:
    """Выполнить именованный запрос с параметрами, не подставляя ввод в SQL."""
    with connect(DATABASE_PATH) as connection:
        return connection.execute(queries()[name], params or {}).fetchall()


def load_data() -> tuple[list[User], list[Link], list[Click]]:
    """Получить объекты из SQLite вместо JSON; JOIN сохраняет владельцев."""
    users = [User.from_data(dict(row)) for row in select("users")]
    owners = {user.id: user for user in users}
    links = [
        Link(
            row["code"],
            row["url"],
            owners[row["owner_id"]],
            date.fromisoformat(row["created_at"]),
            date.fromisoformat(row["expires_at"]),
            bool(row["is_active"]),
        )
        for row in select("links")
    ]
    by_code = {link.code: link for link in links}
    raw_clicks = {row["id"]: row for row in select("click_objects")}
    clicks = []
    for item in select("clicks"):
        row = raw_clicks[item["id"]]
        clicks.append(
            Click(
                row["id"],
                by_code[row["code"]],
                date.fromisoformat(row["clicked_at"]),
                row["source"] or "direct",
            )
        )
    return users, links, clicks


def statistics() -> dict:
    """Все статистические запросы используются на странице статистики."""
    params = {"minimum": 3, "limit": 5, "offset": 0}
    return {
        name: [dict(row) for row in select(name, params)]
        for name in (
            "totals",
            "click_totals",
            "by_link",
            "by_source",
            "popular",
            "recent",
            "by_owner",
            "sources",
        )
    }
