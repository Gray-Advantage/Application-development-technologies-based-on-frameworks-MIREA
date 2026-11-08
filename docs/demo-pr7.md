# ПР7 — карта защиты сокращателя ссылок

Roomly — учебный пример методички. В нашем проекте Room → Link,
User → User, Booking → Click. Аналог доступных помещений — ссылки,
которые включены и действуют на выбранную дату. Отключённые ссылки
не попадают в результат. Срок действия не включает expires_at.

Запуск: `python -m db.import_json`, затем `python manage.py runserver`.
Для демонстрации поиска используйте `/links/available/?date=2026-09-15&q=mirea`.
Статистика: `/links/statistics/`. Исходные даты сохранены из ПР2.

## 25 показателей оценивания из раздела 7.6

| № | Что показать и объяснить | Прямая ссылка |
|---|---|---|
| 1 | users → links → clicks; один пользователь владеет несколькими ссылками | [Таблицы](../sql/schema.sql) |
| 2 | PRIMARY KEY, REFERENCES, RESTRICT, CHECK и допустимый NULL source | [Схема](../sql/schema.sql) |
| 3 | create_schema, IF NOT EXISTS сохраняет таблицы при повторном запуске | [Создание](../db/database.py) |
| 4 | sqlite3.connect, путь DATABASE_PATH, закрытие в finally | [Подключение](../db/database.py) |
| 5 | users перед links перед clicks; executemany и транзакция | [Импорт](../db/import_json.py) |
| 6 | COUNT: 3 пользователя, 5 ссылок, 24 перехода; повторный импорт | [Проверка](../tests/test_sqlite.py) |
| 7 | Запрос users; заменить * на id, username | [SELECT](../sql/queries.sql) |
| 8 | Запрос available; изменить date с 2026-09-15 на 2026-11-08 | [WHERE](../sql/queries.sql) |
| 9 | available: is_active = 1, изменить на 0 и объяснить отключённые ссылки | [Признак состояния](../sql/queries.sql) |
| 10 | links и clicks: JOIN по ключам, LEFT JOIN сохраняет нулевые группы | [JOIN](../sql/queries.sql) |
| 11 | available: is_active AND created_at <= date AND expires_at > date | [Несколько условий](../sql/queries.sql) |
| 12 | totals, click_totals: COUNT; COUNT(column) не считает NULL, пустая выборка даёт 0 | [Подсчёт](../sql/queries.sql) |
| 13 | by_source и by_link: одна строка результата на группу | [GROUP BY](../sql/queries.sql) |
| 14 | popular: HAVING COUNT(*) >= :minimum после группировки | [HAVING](../sql/queries.sql) |
| 15 | select передаёт словарь параметров отдельно от SQL | [Параметры](../db/repository.py) |
| 16 | sqlite3.Row, fetchall и обращение row["code"] вместо числового индекса | [Обработка результата](../db/repository.py), [row_factory](../db/database.py) |
| 17 | links → load_data → SQL → cards → include карточки | [View](../links/views.py), [Шаблон](../links/templates/links/link_list.html) |
| 18 | Включённые ссылки с created_at <= date < expires_at | [Поиск](../links/views.py), [HTML](../links/templates/links/available.html) |
| 19 | Переход с его ссылкой и владельцем | [Сборка объектов](../db/repository.py), [Строка](../clicks/templates/clicks/includes/click_row.html) |
| 20 | request.GET date/q, fromisoformat, параметризованный поиск | [available](../links/views.py) |
| 21 | Агрегаты, группы по ссылке, источнику, владельцу | [statistics](../db/repository.py), [HTML](../links/templates/links/statistics.html) |
| 22 | Временно переименовать cards только в контексте; появится «не найдены»; вернуть | [Контекст](../links/views.py), [Цикл](../links/templates/links/link_list.html) |
| 23 | q=zzzz или дата вне сроков: пустой список; date=abc: сообщение ошибки ввода | [Обработка](../links/views.py), [empty](../links/templates/links/available.html) |
| 24 | В копии запроса заменить owner_id на owner: OperationalError; вернуть owner_id. Неверный JOIN может дать неверные данные без исключения | [SQL](../sql/queries.sql) |
| 25 | /links/available/ → URL → available → select → SQL → cards → HTML | [Маршрут](../links/urls.py), [View](../links/views.py), [SQL](../db/repository.py), [HTML](../links/templates/links/available.html) |

## Чек-лист индивидуального проекта из раздела 7.2

| № | Требование и подтверждение |
|---|---|
| 1 | [Консольная версия сохранена](../main.py), [шаблоны ПР6](../templates/base.html) |
| 2 | [User, Link, Click](../models/__init__.py) |
| 3 | [users, links, clicks](../sql/schema.sql) |
| 4 | [Типы INTEGER, TEXT, CHECK](../sql/schema.sql) |
| 5 | [PRIMARY KEY](../sql/schema.sql) |
| 6 | [REFERENCES](../sql/schema.sql) |
| 7 | [Рабочая база](../data/shortener.sqlite) |
| 8 | [CREATE TABLE](../sql/schema.sql) |
| 9 | [Подключение](../db/database.py) |
| 10 | [PRAGMA foreign_keys](../db/database.py) |
| 11 | [Скрипт импорта](../db/import_json.py) |
| 12 | [JSON источники](../data/users.json), [импорт](../db/import_json.py) |
| 13 | [Повторяемость, счётчики, внешние ключи и откат](../tests/test_sqlite.py) |
| 14 | [14 исполняемых запросов](../sql/queries.sql) |
| 15 | SQLite CLI: `.parameter init`; задать :date, :query, :minimum=3, :limit=5, :offset=0; затем `.read sql/queries.sql` |
| 16 | [users, search, available](../sql/queries.sql) |
| 17 | [links, clicks](../sql/queries.sql) |
| 18 | [totals, click_totals](../sql/queries.sql) |
| 19 | [by_link, by_source, by_owner](../sql/queries.sql) |
| 20 | [popular](../sql/queries.sql) |
| 21 | [Именованные параметры](../db/repository.py) |
| 22 | [row_factory = sqlite3.Row](../db/database.py) |
| 23 | [Список ссылок](../links/views.py) |
| 24 | [Список переходов](../clicks/views.py) |
| 25 | [Поиск доступных ссылок на дату](../links/views.py) |
| 26 | [Статистика](../links/templates/links/statistics.html) |
| 27 | [Навигация](../templates/includes/navigation.html) |
| 28 | [README](../README.md) |
| 29 | `pytest -v`, `python manage.py check`, `flake8`, `ruff check`, `mypy` |
| 30 | `git log --oneline --grep='^PR7:'` |
| 31 | [14 запросов: 2 SELECT, 2 WHERE, 2 JOIN, 2 агрегата, 3 GROUP BY](../sql/queries.sql) |

Практикум предъявляется отдельно. Эта карта подтверждает индивидуальный проект.
