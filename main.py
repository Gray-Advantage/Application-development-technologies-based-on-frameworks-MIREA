"""Сервис сокращения ссылок — консольное приложение.

Точка запуска программы: загрузка объектов из JSON-файлов, меню,
выполнение пользовательских сценариев и сохранение изменённых данных
перед завершением работы.
"""

from datetime import date
from pathlib import Path

from models import Click, Link, User
from models.clicks import (
    DEFAULT_SOURCE,
    count_clicks_by,
    get_total_stats,
    register_click,
    show_link_stats,
    show_total_stats,
)
from models.links import (
    CODE_RULES,
    DEFAULT_LIFETIME_DAYS,
    MAX_LIFETIME_DAYS,
    add_link,
    filter_available_links,
    find_link_by_code,
    find_links,
    find_links_by_owner,
    get_link_status,
    is_code_free,
    parse_code,
    show_links,
    sort_links,
)
from models.users import add_user, find_user_by_id, find_users, show_users
from storage import (
    load_clicks,
    load_links,
    load_users,
    save_clicks,
    save_links,
    save_users,
)
from utils import (
    format_date,
    input_date,
    input_int,
    input_text,
    input_yes_no,
)

DATA_DIR = Path(__file__).parent / "data"
USERS_FILE = DATA_DIR / "users.json"
LINKS_FILE = DATA_DIR / "links.json"
CLICKS_FILE = DATA_DIR / "clicks.json"

MENU_ITEMS = (
    ("1", "Показать ссылки"),
    ("2", "Показать доступные ссылки"),
    ("3", "Найти ссылку"),
    ("4", "Проверить короткий код"),
    ("5", "Сократить ссылку"),
    ("6", "Перейти по короткой ссылке"),
    ("7", "Статистика по ссылке"),
    ("8", "Общая статистика"),
    ("9", "Отключить ссылку"),
    ("10", "Показать пользователей"),
    ("11", "Найти пользователя"),
    ("12", "Добавить пользователя"),
    ("13", "Ссылки пользователя"),
    ("0", "Выход"),
)
SORT_OPTIONS = (
    ("created_at", "по дате создания"),
    ("code", "по короткому коду"),
    ("expires_at", "по сроку действия"),
)


def print_links(links: list[Link], clicks: list[Click], today: date) -> None:
    """Вывести таблицу ссылок с количеством переходов по каждой."""
    show_links(links, count_clicks_by(clicks, "link"), today)


def ask_link(links: list[Link]) -> Link | None:
    """Запросить короткий код и найти ссылку; сообщить, если её нет."""
    code = parse_code(input_text("Короткий код или короткий адрес: "))
    link = find_link_by_code(links, code)
    if link is None:
        print(f"Ссылка с кодом «{code}» не найдена")
    return link


def ask_user(users: list[User]) -> User | None:
    """Запросить ID пользователя и найти его; сообщить, если его нет."""
    user_id = input_int("ID пользователя: ", 1)
    user = find_user_by_id(users, user_id)
    if user is None:
        print(f"Пользователь #{user_id} не найден")
    return user


def handle_show_links(
    links: list[Link], clicks: list[Click], today: date
) -> None:
    """Вывести все ссылки в порядке, выбранном пользователем."""
    for number, (_, title) in enumerate(SORT_OPTIONS, start=1):
        print(f"{number}. {title}")
    choice = input_int(
        "Порядок сортировки (Enter — 1): ", 1, len(SORT_OPTIONS), default=1
    )
    field = SORT_OPTIONS[choice - 1][0]
    print_links(sort_links(links, field), clicks, today)


def handle_find_links(
    links: list[Link], clicks: list[Click], today: date
) -> None:
    """Найти ссылки по части кода или адреса."""
    query = input_text("Часть кода или адреса: ")
    print_links(find_links(links, query), clicks, today)


def handle_check_code(links: list[Link]) -> None:
    """Проверить, свободен ли короткий код."""
    code = parse_code(input_text("Короткий код: "))
    if Link.validate_code(code):
        print(get_link_status(is_code_free(links, code)))
    else:
        print(CODE_RULES)


def create_new_link(
    links: list[Link], users: list[User], today: date
) -> bool:
    """Сократить ссылку; вернуть True, если ссылка создана."""
    owner = ask_user(users)
    if owner is None:
        return False
    url = input_text("Исходный адрес: ")
    code = input_text(
        "Свой короткий код (Enter — сгенерировать): ", allow_empty=True
    )
    lifetime_days = input_int(
        f"Срок действия в днях (Enter — {DEFAULT_LIFETIME_DAYS}): ",
        1,
        MAX_LIFETIME_DAYS,
        default=DEFAULT_LIFETIME_DAYS,
    )
    link = add_link(links, owner, url, today, code, lifetime_days)
    print(f"Создана ссылка: {link}")
    print(f"Действует до: {format_date(link.expires_at)}")
    return True


def open_link(links: list[Link], clicks: list[Click], today: date) -> bool:
    """Перейти по короткой ссылке; вернуть True, если переход учтён."""
    link = ask_link(links)
    if link is None:
        return False
    clicked_at = input_date(
        "Дата перехода ДД.ММ.ГГГГ (Enter — сегодня): ", today
    )
    source = input_text(
        f"Источник перехода (Enter — {DEFAULT_SOURCE}): ", allow_empty=True
    )
    register_click(clicks, link, clicked_at, source)
    print(f"Переход выполнен: {link.url}")
    return True


def handle_link_stats(
    links: list[Link], clicks: list[Click], today: date
) -> None:
    """Вывести статистику по ссылке, выбранной пользователем."""
    link = ask_link(links)
    if link is not None:
        show_link_stats(link, clicks, today)


def handle_deactivate_link(links: list[Link]) -> bool:
    """Отключить ссылку после подтверждения; вернуть True, если отключена."""
    link = ask_link(links)
    if link is None:
        return False
    if not link.is_active:
        print("Ссылка уже отключена")
        return False
    if not input_yes_no(f"Отключить ссылку {link}? (д/н): "):
        print("Отключение отменено")
        return False
    link.deactivate()
    print("Ссылка отключена, статистика переходов сохранена")
    return True


def handle_find_users(users: list[User]) -> None:
    """Найти пользователей по части логина или адреса почты."""
    query = input_text("Часть логина или адреса почты: ")
    show_users(find_users(users, query))


def create_new_user(users: list[User], today: date) -> bool:
    """Добавить пользователя по введённым данным; вернуть True."""
    username = input_text("Логин: ")
    email = input_text("Электронная почта: ")
    user = add_user(users, username, email, today)
    print(f"Пользователь создан: {user}")
    return True


def handle_user_links(
    links: list[Link], users: list[User], clicks: list[Click], today: date
) -> None:
    """Вывести ссылки пользователя, выбранного по ID."""
    user = ask_user(users)
    if user is not None:
        print(f"Ссылки пользователя {user}:")
        print_links(find_links_by_owner(links, user), clicks, today)


def print_menu() -> None:
    """Вывести меню приложения."""
    print()
    print("=== Сервис сокращения ссылок ===")
    for key, title in MENU_ITEMS:
        print(f"{key}. {title}")


def run_action(
    choice: str,
    links: list[Link],
    users: list[User],
    clicks: list[Click],
) -> bool:
    """Выполнить пункт меню; вернуть True, если данные изменились."""
    today = date.today()
    data_changed = False
    if choice == "1":
        handle_show_links(links, clicks, today)
    elif choice == "2":
        print_links(list(filter_available_links(links, today)), clicks, today)
    elif choice == "3":
        handle_find_links(links, clicks, today)
    elif choice == "4":
        handle_check_code(links)
    elif choice == "5":
        data_changed = create_new_link(links, users, today)
    elif choice == "6":
        data_changed = open_link(links, clicks, today)
    elif choice == "7":
        handle_link_stats(links, clicks, today)
    elif choice == "8":
        show_total_stats(get_total_stats(links, users, clicks, today))
    elif choice == "9":
        data_changed = handle_deactivate_link(links)
    elif choice == "10":
        show_users(users)
    elif choice == "11":
        handle_find_users(users)
    elif choice == "12":
        data_changed = create_new_user(users, today)
    elif choice == "13":
        handle_user_links(links, users, clicks, today)
    else:
        print("Такого пункта меню нет")
    return data_changed


def save_data(
    links: list[Link], users: list[User], clicks: list[Click]
) -> None:
    """Сохранить пользователей, ссылки и переходы в JSON-файлы."""
    try:
        save_users(USERS_FILE, users)
        save_links(LINKS_FILE, links)
        save_clicks(CLICKS_FILE, clicks)
    except OSError as error:
        print(f"Не удалось сохранить данные: {error}")
    else:
        print("Изменения сохранены")


def main() -> None:
    """Точка запуска: загрузка объектов, цикл меню и сохранение данных."""
    users = load_users(USERS_FILE)
    links = load_links(LINKS_FILE, users)
    clicks = load_clicks(CLICKS_FILE, links)
    has_changes = False
    try:
        while True:
            print_menu()
            choice = input("Выберите действие: ").strip()
            if choice == "0":
                break
            try:
                if run_action(choice, links, users, clicks):
                    has_changes = True
            except ValueError as error:
                print(f"Ошибка: {error}")
    except (KeyboardInterrupt, EOFError):
        print()
        print("Работа прервана пользователем")
    finally:
        if has_changes:
            save_data(links, users, clicks)
        print("До свидания!")


if __name__ == "__main__":
    main()
