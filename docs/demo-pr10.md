# ПР10. Django Admin и ORM

В сокращателе ссылок используются `Link` (ссылка), `User` (владелец)
и `Click` (переход). Аккаунты админки относятся к `django.contrib.auth`.
У ссылок хранится включённое или отключённое состояние. Истечение срока
вычисляется по дате для уже созданной ссылки. Переходы остаются в журнале
при отключении.

## Подготовка

```bash
python manage.py migrate
python manage.py import_legacy
python manage.py createsuperuser
python manage.py runserver
```

Импорт нужен при первом запуске на чистой базе. Для проверки прав создайте
в админке группу с разрешениями просмотра ссылок, владельцев и переходов.
Назначьте её активному staff-аккаунту. Он увидит списки и карточки, а
действия изменения будут доступны после выдачи соответствующих разрешений
`change`. Для действий с переходами в inline нужны разрешения на `Click`.

## Пункты защиты из раздела 7.3

| № | Что показать |
| --- | --- |
| 1 | [LinkAdmin](../links/admin.py), [UserAdmin](../users/admin.py) и [ClickAdmin](../clicks/admin.py). Посмотреть списки, поиск, фильтры, порядок, размер страницы. |
| 2 | [ClickInline](../links/admin.py) в ссылке и [LinkInline](../users/admin.py) во владельце. Показать цепочку владелец → ссылка → переходы. |
| 3 | [Поля и подписи Link](../links/models.py), [миграция](../links/migrations/0002_admin_labels_and_link_status.py), `showmigrations`. |
| 4 | [copy_status и restore_is_active](../links/migrations/0002_admin_labels_and_link_status.py). Булево значение переносится перед удалением поля. |
| 5 | `python manage.py shell`, `Link.objects.get(pk="mirea")`, `link.owner`, `link.clicks.count()`. |
| 6 | [demo_orm](../links/management/commands/demo_orm.py) показывает create, save и delete в транзакции с откатом. |
| 7 | [link_list](../links/queries.py), ORM строит ленивый QuerySet, который выполняется при обходе. |
| 8 | [click_list](../links/queries.py) фильтрует по дате, коду, владельцу и поисковой строке. |
| 9 | [LinkQuerySet](../links/models.py), [ClickQuerySet](../clicks/models.py), их использование в [запросах](../links/queries.py). |
| 10 | [Валидация фильтров](../clicks/views.py), `/clicks/?date=abc`. |
| 11 | [Список разрешённых сортировок](../links/queries.py), `/clicks/?sort=-date`. |
| 12 | [recent, sources](../links/queries.py) демонстрируют `values`, `distinct` и ограничение выборки. |
| 13 | [click_labels](../links/queries.py) формирует связанные значения через `F` и `annotate`. |
| 14 | [link_detail](../links/views.py) отвечает 404 для `/links/missing/`. |
| 15 | [get_absolute_url](../links/models.py) из [карточки](../links/templates/links/includes/link_card.html) и админки. |
| 16 | Срок зависит от выбранной даты. В качестве вычисления в БД показать [число переходов Count](../links/queries.py). |
| 17 | [statistics](../links/queries.py) рассчитывает включённые, отключённые, доступные и истёкшие ссылки. |
| 18 | [by_link, by_source, by_owner](../links/queries.py) группируют данные и считают количество. |
| 19 | [ClickQuerySet.with_link](../clicks/models.py) загружает ссылку и владельца через JOIN. |
| 20 | На `/clicks/1/` открыть SQL в Debug Toolbar. Найти SELECT с JOIN ссылок и владельцев. |
| 21 | `/clicks/?owner=2&code=mirea&sort=-date&page=2`. Показать [Paginator](../clicks/views.py) и [сохранение querystring](../templates/includes/pagination.html). |
| 22 | [available_on](../links/models.py), `/links/available/?date=2026-09-15`. Показать исключение отключённой или истёкшей ссылки. |
| 23 | Общий [base.html](../templates/base.html) использует подключённый в [settings](../shortener/settings.py) процессор `request` через [пагинацию](../templates/includes/pagination.html). |
| 24 | [Link.Status](../links/models.py), `get_status_display()`, фильтр по статусу админки. |
| 25 | [Связанный список](../clicks/admin.py) показывает владельца ссылки и позволяет по нему искать. |
| 26 | [Проверка доступности](../links/test_admin.py) и [тест одного SQL-запроса](../clicks/tests.py). |
| 27 | [Именованные маршруты](../links/urls.py) и `reverse("links:detail", kwargs={"code": "mirea"})`. |
| 28 | `python manage.py check`, `python manage.py makemigrations --check --dry-run`. |
| 29 | [Тест миграций, импорта и моделей](../clicks/tests.py), `python manage.py showmigrations`. |
| 30 | [Интеграционные тесты](../links/test_admin.py) и [пользовательские сценарии](../clicks/tests.py), `pytest -v`. |

В списке переходов запрос `COUNT` нужен пагинатору, а запросы владельцев
и ссылок заполняют варианты фильтра. На детальной странице обращение к
`click.link.owner` происходит после одного SELECT с JOIN. Это проверяет
`test_related_objects_one_query`.

## Чек-лист 7.2

1. Админка трёх моделей и связи — пункты 1–2.
2. Миграции — пункты 3 и 28–29.
3. Перенос статусов — пункт 4.
4. Менеджеры/QuerySet — пункт 9.
5. Чтение и обработка через ORM — пункты 7–8, 12–13, 17–18.
6. Фильтрация, сортировка, пагинация — пункты 8–11 и 21.
7. Доступность на дату — пункт 22.
8. Статистика по состояниям — пункты 17 и 24.
9. Адрес по slug — пункты 14–15 и 27.
10. Общий контекст шаблонов — пункт 23.
11. Для срока действия используется расчёт по дате и SQL-агрегация — пункт 16.
12. Анализ SQL — пункты 19–20 и 26.
13. Операции через Django Shell — пункты 5–6.
14. Системные проверки — пункт 28.
15. Тесты — пункты 26, 29–30.
16. [README](../README.md).
17. `git log --oneline --grep='^PR10:'`.
