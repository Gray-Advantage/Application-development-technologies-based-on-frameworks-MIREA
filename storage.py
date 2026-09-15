"""Функции сохранения и загрузки объектов в JSON-файлах.

JSON используется для хранения данных, а объекты — для работы
приложения. При загрузке записи превращаются в объекты, при сохранении
объекты превращаются обратно в записи, а связанные объекты заменяются
их идентификаторами.
"""

import json
from collections.abc import Callable
from datetime import date
from pathlib import Path

from models import Click, Link, User
from models.links import find_link_by_code
from models.users import find_user_by_id


def read_json_list(path: Path) -> list[dict]:
    """Прочитать список записей из JSON-файла.

    Если файл отсутствует, повреждён или содержит не список,
    выводится сообщение и возвращается пустой список.
    """
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Файл {path.name} не найден, данные будут созданы заново")
        return []
    except json.JSONDecodeError:
        print(f"Файл {path.name} содержит некорректный JSON")
        return []
    else:
        if isinstance(data, list):
            return data
        print(f"Файл {path.name} должен содержать список записей")
        return []


def write_json_list(path: Path, records: list[dict]) -> None:
    """Записать список записей в JSON-файл.

    Каталог для файла создаётся, если его ещё нет.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=4)


def load_objects(path: Path, build: Callable[[dict], object]) -> list:
    """Прочитать записи из JSON-файла и превратить их в объекты.

    Функция build создаёт объект из одной записи. Некорректные записи
    пропускаются с сообщением, остальные данные загружаются.
    """
    objects = []
    for record in read_json_list(path):
        try:
            objects.append(build(record))
        except (KeyError, TypeError, ValueError) as error:
            print(f"В файле {path.name} пропущена запись: {error}")
    return objects


def link_from_data(data: dict, users: list[User]) -> Link:
    """Создать ссылку из записи JSON, найдя владельца по owner_id."""
    owner = find_user_by_id(users, data["owner_id"])
    if owner is None:
        raise ValueError(f"владелец #{data['owner_id']} не найден")
    return Link(
        code=data["code"],
        url=data["url"],
        owner=owner,
        created_at=date.fromisoformat(data["created_at"]),
        expires_at=date.fromisoformat(data["expires_at"]),
        is_active=data["is_active"],
    )


def click_from_data(data: dict, links: list[Link]) -> Click:
    """Создать переход из записи JSON, найдя ссылку по короткому коду."""
    link = find_link_by_code(links, data["code"])
    if link is None:
        raise ValueError(f"ссылка «{data['code']}» не найдена")
    return Click(
        click_id=data["id"],
        link=link,
        clicked_at=date.fromisoformat(data["clicked_at"]),
        source=data["source"],
    )


def user_to_data(user: User) -> dict:
    """Преобразовать пользователя в запись JSON."""
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "registered_at": user.registered_at.isoformat(),
    }


def link_to_data(link: Link) -> dict:
    """Преобразовать ссылку в запись JSON; владелец заменяется его id."""
    return {
        "code": link.code,
        "url": link.url,
        "owner_id": link.owner.id,
        "created_at": link.created_at.isoformat(),
        "expires_at": link.expires_at.isoformat(),
        "is_active": link.is_active,
    }


def click_to_data(click: Click) -> dict:
    """Преобразовать переход в запись JSON; ссылка заменяется её кодом."""
    return {
        "id": click.id,
        "code": click.link.code,
        "clicked_at": click.clicked_at.isoformat(),
        "source": click.source,
    }


def load_users(path: Path) -> list[User]:
    """Загрузить пользователей из JSON-файла."""
    return load_objects(path, User.from_data)


def load_links(path: Path, users: list[User]) -> list[Link]:
    """Загрузить ссылки и связать их с объектами пользователей."""
    return load_objects(path, lambda data: link_from_data(data, users))


def load_clicks(path: Path, links: list[Link]) -> list[Click]:
    """Загрузить переходы и связать их с объектами ссылок."""
    return load_objects(path, lambda data: click_from_data(data, links))


def save_users(path: Path, users: list[User]) -> None:
    """Сохранить пользователей в JSON-файл."""
    write_json_list(path, [user_to_data(user) for user in users])


def save_links(path: Path, links: list[Link]) -> None:
    """Сохранить ссылки в JSON-файл."""
    write_json_list(path, [link_to_data(link) for link in links])


def save_clicks(path: Path, clicks: list[Click]) -> None:
    """Сохранить переходы в JSON-файл."""
    write_json_list(path, [click_to_data(click) for click in clicks])
