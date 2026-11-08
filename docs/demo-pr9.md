# ПР9 — карта защиты сокращателя ссылок

Наши сущности: User (владелец), Link (ссылка), Click (переход).
Roomly в методичке служит примером. Поиск доступных помещений адаптирован
в поиск включённых ссылок, действующих на заданную дату.

Подготовка: `python manage.py migrate`, `python manage.py import_legacy`,
`python manage.py runserver`. База ПР7 `data/shortener.sqlite` сохранена;
ORM работает с отдельной `db.sqlite3`. Не подменять одну базу другой.

## 30 показателей оценивания из раздела 7.3

| № | Что показать за 5 минут | Код и действие |
|---|---|---|
| 1 | Модель, типы полей и ограничения | [Link](../links/models.py), [User](../users/models.py), [Click](../clicks/models.py). Изменить max_length, выполнить makemigrations, затем migrate |
| 2 | ForeignKey, on_delete и обратные связи | [Модели](../links/models.py). link.owner и owner.links.all(); PROTECT сохраняет историю |
| 3 | Прямая и обратная связь | [ForeignKey и related_name](../clicks/models.py), [демонстрация](../links/management/commands/demo_orm.py). click.link.owner, link.clicks.all(), owner.links.all(); при смене related_name меняется имя обратного доступа |
| 4 | Создание и применение миграций | [Модель](../links/models.py), [миграция](../links/migrations/0001_initial.py), [зависимости](../clicks/migrations/0001_initial.py). Изменить параметр поля, выполнить makemigrations и migrate; showmigrations показывает `[X]` |
| 5 | Создать объект | [Безопасная CRUD-демонстрация](../links/management/commands/demo_orm.py). `python manage.py demo_orm` |
| 6 | Изменить поле и вызвать save | [deactivate](../links/models.py). refresh_from_db подтверждает сохранение |
| 7 | Удалить тестовый объект | [delete и откат](../links/management/commands/demo_orm.py). Сначала дочерний Click, затем Link и User |
| 8 | QuerySet и filter | [Q01 и Q02](../links/queries.py). В shell `Link.objects.all()` и `.filter(is_active=True)` |
| 9 | Фильтр по связанному полю | [Q15 и click_list](../links/queries.py). link__url / link__owner__username; двойное подчёркивание — переход по связи |
| 10 | Несколько условий | [click_list](../links/queries.py). `/clicks/?owner=2&code=mirea&date=2026-09-02` |
| 11 | Проверка ввода | [clicks](../clicks/views.py), [available](../links/views.py). owner=bad, date=abc — сообщение, без 500 |
| 12 | Сортировка по полю и направлению | [fields](../links/queries.py). `/clicks/?sort=-date` и `sort=date` |
| 13 | Разрешённые поля сортировки | [click_list](../links/queries.py). sort=bad даёт порядок по дате и id |
| 14 | values и структура словаря | [Q10 и Q17](../links/queries.py). Добавить поле в values, вывести list(queryset) |
| 15 | annotate и F | [Q17 click_labels](../links/queries.py), [HTML](../links/templates/links/statistics.html). owner=F("link__owner__username") |
| 16 | Отдельный объект или 404 | [get_object_or_404](../links/views.py). `/links/mirea/` и `/links/missing/` |
| 17 | Агрегирующие функции | [Q04/Q05](../links/queries.py). COUNT, MIN, MAX; сопоставить с 5 ссылками и 24 переходами |
| 18 | Статистика по связям | [Q06/Q09](../links/queries.py). Изменить order_by("-total") на order_by("total") |
| 19 | select_related и число запросов | [click_detail](../clicks/views.py). `/clicks/1/`, панель Debug Toolbar → SQL: JOIN ссылок и владельцев. [Тест одного запроса](../clicks/tests.py) |
| 20 | Только нужные поля | [Q17](../links/queries.py). `/links/statistics/`, Debug Toolbar → SQL: поля id/code/owner. values формирует словари |
| 21 | Контекст и шаблон | [cards](../links/views.py), [цикл](../links/templates/links/link_list.html). Переименовать в обоих местах; только в одном — пустой вывод |
| 22 | Размер страницы | [Paginator(result, 5)](../clicks/views.py). Заменить 5 на 3; меняется число страниц |
| 23 | Навигация | [Пагинация](../templates/includes/pagination.html). Первая/последняя страницы; page=abc → первая, page=999 → последняя |
| 24 | Сохранение параметров | [querystring](../templates/includes/pagination.html). `/clicks/?code=mirea&sort=-date`, нажать страницу 2 |
| 25 | Совместная работа | [click_list](../links/queries.py), [view](../clicks/views.py). Сначала фильтрация, потом сортировка, потом Paginator |
| 26 | Объекты без дочерних записей | [Q06 by_link](../links/queries.py), [тест zero](../clicks/tests.py). LEFT JOIN и Count сохраняют нулевую группу |
| 27 | exclude | [Q13 и click_list](../links/queries.py). `/clicks/?active=1` исключает переходы по отключённым ссылкам |
| 28 | Ограничение выборки | [Q10 recent](../links/queries.py). [:5] — LIMIT 5; изменить на [:3] |
| 29 | get и исключения | [demo_orm](../links/management/commands/demo_orm.py). В shell `Link.objects.get(pk="mirea")`; missing → DoesNotExist, `.get(is_active=True)` при нескольких → MultipleObjectsReturned |
| 30 | Полный путь ORM → HTML | [URL](../clicks/urls.py) → [view](../clicks/views.py) → [query](../links/queries.py) → [HTML](../clicks/templates/clicks/click_list.html) |

## 31 требование чек-листа раздела 7.2

| № | Где подтверждено |
|---|---|
| 1 | [Сохранённая консольная версия](../main.py), [шаблоны](../templates/base.html) |
| 2 | [User](../users/models.py), [Link](../links/models.py), [Click](../clicks/models.py) |
| 3 | [Типы полей](../links/models.py) |
| 4 | [unique/default/null/CheckConstraint](../links/models.py), [source](../clicks/models.py) |
| 5 | [code как PK](../links/models.py), [автоматический BigAutoField](../users/migrations/0001_initial.py) |
| 6 | [ForeignKey владельца](../links/models.py), [ForeignKey ссылки](../clicks/models.py) |
| 7 | [PROTECT и related_name](../clicks/models.py) |
| 8 | [users](../users/migrations/0001_initial.py), [links](../links/migrations/0001_initial.py), [clicks](../clicks/migrations/0001_initial.py) |
| 9 | `python manage.py showmigrations`: users/links/clicks `[X]` |
| 10 | [Обратная связь link.clicks](../links/management/commands/demo_orm.py) |
| 11 | [Q01 link_list](../links/queries.py) |
| 12 | [Q18 link_detail](../links/views.py), [Q20 click_detail](../clicks/views.py) |
| 13 | [create/get/save/delete](../links/management/commands/demo_orm.py) |
| 14 | [Q12 disabled](../links/queries.py) |
| 15 | [Q02 available_links и Q03 click_list](../links/queries.py) |
| 16 | [Q15 education](../links/queries.py) |
| 17 | [Q13 unexpired](../links/queries.py) |
| 18 | [Q14 telegram](../links/queries.py) |
| 19 | [Q02 поиск по code/url, Q03 по источнику/URL/владельцу](../links/queries.py) |
| 20 | [Q01, Q03, Q09](../links/queries.py) |
| 21 | [select_related в Q01/Q03](../links/queries.py), [деталь перехода](../clicks/views.py) |
| 22 | [values в Q10/Q11/Q17](../links/queries.py) |
| 23 | [aggregate в Q04/Q05](../links/queries.py) |
| 24 | [annotate, Count, F в Q06–Q09/Q17](../links/queries.py) |
| 25 | [Paginator](../clicks/views.py) |
| 26 | [Навигация с querystring](../templates/includes/pagination.html) |
| 27 | [Контекст](../clicks/views.py), [HTML](../clicks/templates/clicks/click_list.html) |
| 28 | [Ошибки ввода и 404](../clicks/views.py), [empty](../clicks/templates/clicks/click_list.html) |
| 29 | [Интеграционные тесты](../clicks/tests.py), `python manage.py check` |
| 30 | [README](../README.md), `git log --oneline --grep='^PR9:'` |
| 31 | [17 запросов Q01–Q17](../links/queries.py), [Q18](../links/views.py), [Q19/Q20](../clicks/views.py). Это самостоятельные выражения, а не подсчёт вызовов в одной цепочке |

## Материалы для быстрого запуска и демонстрации

`python manage.py demo_orm` показывает создание, get, save, обратные связи
и удаление; транзакция откатывается. Для shell: `python manage.py shell`.
При изменении моделей создавать и применять миграции; временные изменения
для показа вернуть после демонстрации.

Исходная база читается только командой [import_legacy](../links/management/commands/import_legacy.py).
Она создаёт резервную копию, сохраняет ключи и проверяет конфликты. Старые
[SQL-модули](../db/repository.py) оставлены как материал ПР7 и не вызываются
веб-представлениями ПР9. Материалы Яндекс Практикума предъявляются отдельно.
