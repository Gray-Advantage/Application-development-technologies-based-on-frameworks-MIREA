"""Сервис сокращения ссылок — консольное приложение.

Точка запуска программы: загрузка данных, меню и вызов функций
проекта в зависимости от выбора пользователя.
"""

from datetime import date
from pathlib import Path

from clicks import (
    DEFAULT_SOURCE,
    POPULAR_CLICKS,
    count_by_field,
    delete_link_clicks,
    get_clicks_per_day,
    get_total_stats,
    is_popular,
    iter_link_clicks,
    register_click,
)
from links import (
    CODE_RULES,
    DEFAULT_LIFETIME_DAYS,
    MAX_LIFETIME_DAYS,
    add_link,
    build_short_url,
    delete_link,
    filter_active_links,
    find_links,
    get_days_left,
    get_days_passed,
    get_lifetime_status,
    get_link_status,
    is_code_free,
    is_link_active,
    is_valid_code,
    parse_code,
    sort_links,
)
from storage import load_clicks, load_links, save_clicks, save_links
from utils import (
    format_date,
    input_date,
    input_int,
    input_text,
    input_yes_no,
)

DATA_DIR = Path(__file__).parent / "data"
LINKS_FILE = DATA_DIR / "links.json"
CLICKS_FILE = DATA_DIR / "clicks.json"
URL_PREVIEW_LENGTH = 45

MENU_ITEMS = (
    ("1", "Показать ссылки"),
    ("2", "Показать активные ссылки"),
    ("3", "Найти ссылку"),
    ("4", "Проверить короткий код"),
    ("5", "Сократить ссылку"),
    ("6", "Перейти по короткой ссылке"),
    ("7", "Статистика по ссылке"),
    ("8", "Общая статистика"),
    ("9", "Удалить ссылку"),
    ("0", "Выход"),
)
SORT_OPTIONS = (
    ("created_at", "по дате создания"),
    ("code", "по короткому коду"),
    ("expires_at", "по сроку действия"),
)


def show_links(links: list[dict], clicks: list[dict], today: date) -> None:
    """Вывести ссылки в виде таблицы."""
    if not links:
        print("Ссылки не найдены")
        return
    counts = count_by_field(clicks, "code")
    print(
        f"{'Код':<14}{'Переходы':>9}  "
        f"{'Действует до':<14}{'Статус':<9}Адрес"
    )
    for link in links:
        url = link["url"]
        if len(url) > URL_PREVIEW_LENGTH:
            url = url[:URL_PREVIEW_LENGTH - 3] + "..."
        status = "активна" if is_link_active(link, today) else "истекла"
        print(
            f"{link['code']:<14}{counts.get(link['code'], 0):>9}  "
            f"{format_date(link['expires_at']):<14}{status:<9}{url}"
        )


def show_link_card(link: dict, clicks: list[dict], today: date) -> None:
    """Вывести подробные сведения и статистику по ссылке."""
    sources = count_by_field(iter_link_clicks(clicks, link["code"]), "source")
    clicks_count = sum(sources.values())
    days_left = get_days_left(link, today)
    clicks_per_day = get_clicks_per_day(
        clicks_count, get_days_passed(link, today)
    )

    print(f"Исходный адрес: {link['url']}")
    print(f"Короткий адрес: {build_short_url(link['code'])}")
    print(f"Дата создания: {format_date(link['created_at'])}")
    print(f"Действует до: {format_date(link['expires_at'])}")
    print(f"Осталось дней: {max(days_left, 0)}")
    print(f"Переходов: {clicks_count}")
    print(f"Переходов в день: {clicks_per_day:.2f}")
    print(get_lifetime_status(days_left))
    if is_popular(clicks_count, days_left):
        print(f"Ссылка популярна: не менее {POPULAR_CLICKS} переходов")
    else:
        print(f"Ссылка пока не набрала {POPULAR_CLICKS} переходов")

    if sources:
        print("Источники переходов:")
        ranked_sources = sorted(
            sources.items(), key=lambda item: item[1], reverse=True
        )
        for source, count in ranked_sources:
            print(f"  {source}: {count}")


def show_total_stats(stats: dict) -> None:
    """Вывести общую статистику сервиса."""
    print(f"Всего ссылок: {stats['links']}")
    print(f"Активных ссылок: {stats['active_links']}")
    print(f"Всего переходов: {stats['clicks']}")
    print(f"Уникальных источников: {stats['sources']}")
    if not stats["top_links"]:
        return
    print("Самые популярные ссылки:")
    for place, (code, count) in enumerate(stats["top_links"], start=1):
        print(f"  {place}. {build_short_url(code)} — {count}")


def ask_code() -> str:
    """Запросить короткий код или полный короткий адрес."""
    return parse_code(input_text("Короткий код или короткий адрес: "))


def handle_show_links(
    links: dict[str, dict], clicks: list[dict], today: date
) -> None:
    """Вывести все ссылки в порядке, выбранном пользователем."""
    for number, (_, title) in enumerate(SORT_OPTIONS, start=1):
        print(f"{number}. {title}")
    choice = input_int(
        "Порядок сортировки (Enter — 1): ", 1, len(SORT_OPTIONS), default=1
    )
    field = SORT_OPTIONS[choice - 1][0]
    show_links(sort_links(links, field), clicks, today)


def handle_find_links(
    links: dict[str, dict], clicks: list[dict], today: date
) -> None:
    """Найти ссылки по части кода или адреса."""
    query = input_text("Часть кода или адреса: ")
    show_links(find_links(links, query), clicks, today)


def handle_check_code(links: dict[str, dict]) -> None:
    """Проверить, свободен ли короткий код."""
    code = ask_code()
    if is_valid_code(code):
        print(get_link_status(is_code_free(links, code)))
    else:
        print(CODE_RULES)


def handle_create_link(links: dict[str, dict], today: date) -> None:
    """Создать короткую ссылку и сохранить ссылки в файл."""
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
    link = add_link(links, url, today, code, lifetime_days)
    save_links(LINKS_FILE, links)
    print(f"Короткая ссылка: {build_short_url(link['code'])}")
    print(f"Действует до: {format_date(link['expires_at'])}")


def handle_open_link(
    links: dict[str, dict], clicks: list[dict], today: date
) -> None:
    """Зарегистрировать переход по короткой ссылке и сохранить его."""
    code = ask_code()
    url = links[code]["url"]
    clicked_at = input_date(
        "Дата перехода ДД.ММ.ГГГГ (Enter — сегодня): ", today
    )
    source = input_text(
        f"Источник перехода (Enter — {DEFAULT_SOURCE}): ", allow_empty=True
    )
    register_click(links, clicks, code, clicked_at, source)
    save_clicks(CLICKS_FILE, clicks)
    print(f"Переход выполнен: {url}")


def handle_link_stats(
    links: dict[str, dict], clicks: list[dict], today: date
) -> None:
    """Вывести статистику по ссылке, выбранной пользователем."""
    show_link_card(links[ask_code()], clicks, today)


def handle_delete_link(links: dict[str, dict], clicks: list[dict]) -> None:
    """Удалить ссылку вместе с её переходами и сохранить данные."""
    code = ask_code()
    url = links[code]["url"]
    if not input_yes_no(f"Удалить ссылку на {url}? (д/н): "):
        print("Удаление отменено")
        return
    delete_link(links, code)
    removed_count = delete_link_clicks(clicks, code)
    save_links(LINKS_FILE, links)
    save_clicks(CLICKS_FILE, clicks)
    print(f"Ссылка удалена, удалено переходов: {removed_count}")


def print_menu() -> None:
    """Вывести меню приложения."""
    print()
    print("=== Сервис сокращения ссылок ===")
    for key, title in MENU_ITEMS:
        print(f"{key}. {title}")


def run_action(
    choice: str, links: dict[str, dict], clicks: list[dict]
) -> None:
    """Выполнить пункт меню, выбранный пользователем."""
    today = date.today()
    if choice == "1":
        handle_show_links(links, clicks, today)
    elif choice == "2":
        show_links(list(filter_active_links(links, today)), clicks, today)
    elif choice == "3":
        handle_find_links(links, clicks, today)
    elif choice == "4":
        handle_check_code(links)
    elif choice == "5":
        handle_create_link(links, today)
    elif choice == "6":
        handle_open_link(links, clicks, today)
    elif choice == "7":
        handle_link_stats(links, clicks, today)
    elif choice == "8":
        show_total_stats(get_total_stats(links, clicks, today))
    elif choice == "9":
        handle_delete_link(links, clicks)
    else:
        print("Такого пункта меню нет")


def main() -> None:
    """Точка запуска приложения: загрузка данных и цикл меню."""
    links = load_links(LINKS_FILE)
    clicks = load_clicks(CLICKS_FILE)
    try:
        while True:
            print_menu()
            choice = input("Выберите действие: ").strip()
            if choice == "0":
                break
            try:
                run_action(choice, links, clicks)
            except KeyError as error:
                print(f"Ссылка с кодом «{error.args[0]}» не найдена")
            except ValueError as error:
                print(f"Ошибка: {error}")
            except OSError as error:
                print(f"Не удалось сохранить данные: {error}")
    except (KeyboardInterrupt, EOFError):
        print()
        print("Работа прервана пользователем")
    finally:
        print("До свидания!")


if __name__ == "__main__":
    main()
