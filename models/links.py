"""Класс короткой ссылки и функции работы с коллекцией ссылок."""

import hashlib
import string
from collections.abc import Iterator
from datetime import date, timedelta

from utils import format_date

from .users import User

SERVICE_DOMAIN = "sl.mirea"
SHORT_URL_PREFIX = f"https://{SERVICE_DOMAIN}/"
CODE_LENGTH = 6
MIN_CODE_LENGTH = 3
MAX_CODE_LENGTH = 30
DEFAULT_LIFETIME_DAYS = 30
MAX_LIFETIME_DAYS = 3650
EXPIRING_SOON_DAYS = 7
URL_PREVIEW_LENGTH = 40
ALLOWED_SCHEMES = ("http://", "https://")
ALLOWED_CODE_CHARS = set(string.ascii_letters + string.digits + "-_")
SORT_FIELDS = ("created_at", "code", "expires_at")
CODE_RULES = (
    f"Код должен содержать от {MIN_CODE_LENGTH} до {MAX_CODE_LENGTH} "
    "символов: латинские буквы, цифры, «-» и «_»"
)


class Link:
    """Короткая ссылка, принадлежащая пользователю."""

    def __init__(
        self,
        code: str,
        url: str,
        owner: User,
        created_at: date,
        expires_at: date,
        is_active: bool = True,
    ) -> None:
        """Создать объект короткой ссылки."""
        self.code = code
        self.url = url
        self.owner = owner
        self.created_at = created_at
        self.expires_at = expires_at
        self.is_active = is_active

    @property
    def short_url(self) -> str:
        """Полный короткий адрес ссылки."""
        return SHORT_URL_PREFIX + self.code

    def days_left(self, today: date) -> int:
        """Вернуть количество дней до окончания срока действия."""
        return (self.expires_at - today).days

    def days_passed(self, today: date) -> int:
        """Вернуть количество дней, прошедших с создания ссылки."""
        return (today - self.created_at).days

    def is_available(self, today: date) -> bool:
        """Проверить, что ссылка включена и её срок действия не истёк."""
        return self.is_active and self.days_left(today) > 0

    def get_state(self, today: date) -> str:
        """Вернуть состояние ссылки с учётом отключения и срока действия."""
        days_left = self.days_left(today)
        if not self.is_active:
            state = "отключена"
        elif days_left > EXPIRING_SOON_DAYS:
            state = "активна"
        elif days_left > 0:
            state = "скоро истекает"
        else:
            state = "истекла"
        return state

    def deactivate(self) -> None:
        """Отключить ссылку: переходы по ней становятся невозможны."""
        self.is_active = False

    def __str__(self) -> str:
        """Вернуть строковое представление ссылки."""
        return (
            f"{self.short_url} → {self.url} "
            f"(владелец: {self.owner.username})"
        )

    @staticmethod
    def validate_url(url: str) -> bool:
        """Проверить, что строка похожа на веб-адрес.

        Адрес должен начинаться с http:// или https://, не содержать
        пробелов и включать доменное имя с точкой.
        """
        if not url.startswith(ALLOWED_SCHEMES) or " " in url:
            return False
        host = url.split("://", 1)[1].split("/", 1)[0]
        return "." in host

    @staticmethod
    def validate_code(code: str) -> bool:
        """Проверить длину короткого кода и допустимость его символов."""
        has_valid_length = MIN_CODE_LENGTH <= len(code) <= MAX_CODE_LENGTH
        return has_valid_length and set(code) <= ALLOWED_CODE_CHARS


def get_link_status(is_available: bool) -> str:
    """Вернуть текстовый статус короткого кода."""
    if is_available:
        return "Короткий код свободен, ссылку можно создать"
    return "Короткий код уже занят"


def find_link_by_code(links: list[Link], code: str) -> Link | None:
    """Найти ссылку по короткому коду; вернуть None, если её нет."""
    for link in links:
        if link.code == code:
            return link
    return None


def is_code_free(links: list[Link], code: str) -> bool:
    """Проверить, что короткий код не занят другой ссылкой."""
    return find_link_by_code(links, code) is None


def generate_code(links: list[Link], url: str) -> str:
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
    links: list[Link],
    owner: User,
    url: str,
    created_at: date,
    code: str = "",
    lifetime_days: int = DEFAULT_LIFETIME_DAYS,
) -> Link:
    """Создать короткую ссылку пользователя и добавить её в коллекцию.

    Если код не задан, он генерируется автоматически.
    При некорректных данных возбуждается ValueError.
    """
    url = url.strip()
    code = code.strip()
    if not Link.validate_url(url):
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
    elif not Link.validate_code(code):
        raise ValueError(CODE_RULES)
    elif not is_code_free(links, code):
        raise ValueError(get_link_status(False))

    expires_at = created_at + timedelta(days=lifetime_days)
    link = Link(code, url, owner, created_at, expires_at)
    links.append(link)
    return link


def parse_code(value: str) -> str:
    """Получить короткий код из кода или полного короткого адреса."""
    value = value.strip()
    if value.startswith(SHORT_URL_PREFIX):
        return value[len(SHORT_URL_PREFIX):]
    return value


def find_links(links: list[Link], query: str) -> list[Link]:
    """Найти ссылки, код или адрес которых содержит подстроку query.

    Поиск выполняется без учёта регистра.
    """
    query = query.strip().lower()
    found = []
    for link in links:
        if query in link.code.lower() or query in link.url.lower():
            found.append(link)
    return found


def find_links_by_owner(links: list[Link], owner: User) -> list[Link]:
    """Вернуть ссылки, владельцем которых является пользователь owner."""
    return [link for link in links if link.owner is owner]


def filter_available_links(
    links: list[Link], today: date
) -> Iterator[Link]:
    """Выдавать по одной ссылки, по которым можно перейти."""
    for link in links:
        if link.is_available(today):
            yield link


def sort_links(links: list[Link], field: str = "created_at") -> list[Link]:
    """Вернуть новый список ссылок, упорядоченный по атрибуту field."""
    if field not in SORT_FIELDS:
        raise ValueError(f"Сортировка по полю «{field}» не поддерживается")
    return sorted(links, key=lambda link: getattr(link, field))


def show_links(
    links: list[Link], clicks_count: dict[Link, int], today: date
) -> None:
    """Вывести ссылки в виде таблицы.

    clicks_count содержит количество переходов по каждой ссылке.
    """
    if not links:
        print("Ссылки не найдены")
        return
    print(
        f"{'Код':<14}{'Переходы':>9}  {'Действует до':<14}"
        f"{'Состояние':<16}{'Владелец':<15}Адрес"
    )
    for link in links:
        url = link.url
        if len(url) > URL_PREVIEW_LENGTH:
            url = url[:URL_PREVIEW_LENGTH - 3] + "..."
        print(
            f"{link.code:<14}{clicks_count.get(link, 0):>9}  "
            f"{format_date(link.expires_at):<14}"
            f"{link.get_state(today):<16}{link.owner.username:<15}{url}"
        )
