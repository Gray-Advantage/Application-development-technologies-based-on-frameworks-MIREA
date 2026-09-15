"""Функции сохранения и загрузки данных в JSON-файлах."""

import json
from pathlib import Path


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


def load_links(path: Path) -> dict[str, dict]:
    """Загрузить ссылки и вернуть словарь, где ключ — короткий код."""
    links = {}
    for record in read_json_list(path):
        try:
            links[record["code"]] = record
        except (KeyError, TypeError):
            print(f"В файле {path.name} пропущена некорректная запись")
    return links


def save_links(path: Path, links: dict[str, dict]) -> None:
    """Сохранить ссылки в JSON-файл в виде списка."""
    write_json_list(path, list(links.values()))


def load_clicks(path: Path) -> list[dict]:
    """Загрузить переходы из JSON-файла."""
    return read_json_list(path)


def save_clicks(path: Path, clicks: list[dict]) -> None:
    """Сохранить переходы в JSON-файл."""
    write_json_list(path, clicks)
