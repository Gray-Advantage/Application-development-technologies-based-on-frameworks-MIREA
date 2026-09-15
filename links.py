"""Функции для работы с короткими ссылками."""

import hashlib
import string
from collections.abc import Iterator
from datetime import date, timedelta

SERVICE_DOMAIN = "sl.mirea"
CODE_LENGTH = 6
MIN_CODE_LENGTH = 3
MAX_CODE_LENGTH = 30
DEFAULT_LIFETIME_DAYS = 30
MAX_LIFETIME_DAYS = 3650
EXPIRING_SOON_DAYS = 7
ALLOWED_SCHEMES = ("http://", "https://")
ALLOWED_CODE_CHARS = set(string.ascii_letters + string.digits + "-_")
SORT_FIELDS = ("created_at", "code", "expires_at")
CODE_RULES = (
    f"Код должен содержать от {MIN_CODE_LENGTH} до {MAX_CODE_LENGTH} "
    "символов: латинские буквы, цифры, «-» и «_»"
)


def get_link_status(is_available):
    """Вернуть текстовый статус короткого кода."""
    if is_available:
        return "Короткий код свободен, ссылку можно создать"
    return "Короткий код уже занят"


def is_valid_url(url: str) -> bool:
    """Проверить, что строка похожа на веб-адрес.

    Адрес должен начинаться с http:// или https://, не содержать
    пробелов и включать доменное имя с точкой.
    """
    if not url.startswith(ALLOWED_SCHEMES) or " " in url:
        return False
    host = url.split("://", 1)[1].split("/", 1)[0]
    return "." in host


def is_valid_code(code: str) -> bool:
    """Проверить длину короткого кода и допустимость его символов."""
    has_valid_length = MIN_CODE_LENGTH <= len(code) <= MAX_CODE_LENGTH
    return has_valid_length and set(code) <= ALLOWED_CODE_CHARS


def is_code_free(links: dict[str, dict], code: str) -> bool:
    """Проверить, что короткий код не занят другой ссылкой."""
    return code not in links


def generate_code(links: dict[str, dict], url: str) -> str:
    """Сгенерировать свободный короткий код для адреса.

    Код — начало MD5-хеша адреса. Если такой код уже занят,
    к адресу добавляется номер попытки и хеш вычисляется заново.
    """
    attempt = 0
    while True:
        source = url if attempt == 0 else f"{url}#{attempt}"
        code = hashlib.md5(source.encode("utf-8")).hexdigest()[:CODE_LENGTH]
        if is_code_free(links, code):
            return code
        attempt += 1


def add_link(
    links: dict[str, dict],
    url: str,
    created_at: date,
    code: str = "",
    lifetime_days: int = DEFAULT_LIFETIME_DAYS,
) -> dict:
    """Создать короткую ссылку и добавить её в словарь links.

    Если код не задан, он генерируется автоматически.
    При некорректных данных возбуждается ValueError.
    """
    url = url.strip()
    code = code.strip()
    if not is_valid_url(url):
        raise ValueError(
            "Адрес должен начинаться с http:// или https:// "
            "и содержать доменное имя"
        )
    if lifetime_days < 1 or lifetime_days > MAX_LIFETIME_DAYS:
        raise ValueError(
            f"Срок действия должен быть от 1 до {MAX_LIFETIME_DAYS} дней"
        )
    if not code:
        code = generate_code(links, url)
    elif not is_valid_code(code):
        raise ValueError(CODE_RULES)
    elif not is_code_free(links, code):
        raise ValueError(get_link_status(False))

    expires_at = created_at + timedelta(days=lifetime_days)
    link = {
        "code": code,
        "url": url,
        "created_at": created_at.isoformat(),
        "expires_at": expires_at.isoformat(),
    }
    links[code] = link
    return link


def delete_link(links: dict[str, dict], code: str) -> dict:
    """Удалить ссылку по короткому коду и вернуть её данные.

    Если ссылки нет, возбуждается KeyError.
    """
    return links.pop(code)


def build_short_url(code: str) -> str:
    """Сформировать полный короткий адрес по коду."""
    return f"https://{SERVICE_DOMAIN}/{code}"


def parse_code(value: str) -> str:
    """Получить короткий код из кода или полного короткого адреса."""
    value = value.strip()
    prefix = build_short_url("")
    if value.startswith(prefix):
        return value[len(prefix):]
    return value


def find_links(links: dict[str, dict], query: str) -> list[dict]:
    """Найти ссылки, код или адрес которых содержит подстроку query.

    Поиск выполняется без учёта регистра.
    """
    query = query.strip().lower()
    found = []
    for link in links.values():
        if query in link["code"].lower() or query in link["url"].lower():
            found.append(link)
    return found


def get_days_left(link: dict, today: date) -> int:
    """Вернуть количество дней до окончания срока действия ссылки."""
    expires_at = date.fromisoformat(link["expires_at"])
    return (expires_at - today).days


def get_days_passed(link: dict, today: date) -> int:
    """Вернуть количество дней, прошедших с создания ссылки."""
    created_at = date.fromisoformat(link["created_at"])
    return (today - created_at).days


def is_link_active(link: dict, today: date) -> bool:
    """Проверить, что срок действия ссылки не истёк."""
    return get_days_left(link, today) > 0


def get_lifetime_status(days_left: int) -> str:
    """Вернуть текстовое состояние срока действия ссылки."""
    if days_left > EXPIRING_SOON_DAYS:
        lifetime_status = "Ссылка активна"
    elif days_left > 0:
        lifetime_status = "Срок действия ссылки скоро истекает"
    else:
        lifetime_status = "Срок действия ссылки истёк"
    return lifetime_status


def filter_active_links(
    links: dict[str, dict], today: date
) -> Iterator[dict]:
    """Выдавать по одной ссылки, срок действия которых не истёк."""
    for link in links.values():
        if is_link_active(link, today):
            yield link


def sort_links(
    links: dict[str, dict], field: str = "created_at"
) -> list[dict]:
    """Вернуть список ссылок, упорядоченный по полю field.

    Даты хранятся в формате ГГГГ-ММ-ДД, поэтому сортировка строк
    совпадает с сортировкой по времени.
    """
    if field not in SORT_FIELDS:
        raise ValueError(f"Сортировка по полю «{field}» не поддерживается")
    return sorted(links.values(), key=lambda link: link[field])
