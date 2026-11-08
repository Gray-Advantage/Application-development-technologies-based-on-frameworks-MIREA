# ПР6: что показывать на защите

Проект: сервис сокращения ссылок. Коммит работы — «ПР 6», тег `pr6`.
Все пункты показываются на текущем состоянии репозитория.

## Перед защитой

```bash
python manage.py check
```

```bash
python manage.py runserver
```

Открыть в браузере: `/`, `/links/`, `/links/mirea/`, `/links/nosuchcode/`,
`/clicks/`, `/clicks/4/`, `/clicks/999/`.

## Таблица оценивания (§7.6), 25 показателей

| №  | Показатель                             | Где смотреть                                                                                                                                                                                                           | Что сказать                                                                                                                                                                                                    |
|----|----------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | Запуск и проверка проекта              | `manage.py`                                                                                                                                                                                                            | `manage.py check` проверяет конфигурацию без запуска, `manage.py runserver` поднимает сервер разработки                                                                                                        |
| 2  | Формирование главной страницы          | `homepage/urls.py:10` → `homepage/views.py:7` → `homepage/templates/homepage/index.html`                                                                                                                               | запрос `/` доходит до `index()`, та вызывает `render()` с шаблоном, шаблон наследует `base.html`, готовый HTML уходит браузеру                                                                                 |
| 3  | Формирование списка ссылок             | `links/views.py:31–43`, `links/templates/links/link_list.html:10`                                                                                                                                                      | view загружает данные через `load_all()`, считает переходы, собирает список `cards` и передаёт его в контексте; вывод нескольких ссылок — цикл `{% for %}` в шаблоне                                           |
| 4  | Страница отдельной ссылки              | `links/urls.py:11`, `links/views.py:46–62`, `links/templates/links/link_detail.html`                                                                                                                                   | код из адреса приходит в параметр `code`, объект находит `find_link_by_code()`, в шаблоне используются `card.link.short_url`, `url`, `owner`, даты и статистика                                                |
| 5  | Формирование списка переходов          | `clicks/views.py:22–30`, `clicks/templates/clicks/click_list.html:11`, `includes/click_row.html`                                                                                                                       | список `rows` передаётся в контексте, а HTML одной записи формирует включаемый шаблон `click_row.html`                                                                                                         |
| 6  | Страница отдельного перехода           | `clicks/views.py:33–48`, `clicks/templates/clicks/click_detail.html`                                                                                                                                                   | переход находит `find_click_by_id()`; при несуществующем идентификаторе `row` равен `None`, шаблон показывает «Переход не найден», а ответ получает статус 404 (`clicks/views.py:47`)                          |
| 7  | Организация переходов между страницами | `templates/includes/navigation.html:2–4`, `links/.../link_card.html:4`, `clicks/.../click_row.html:2,8`                                                                                                                | адреса не прописаны руками: ссылки строит тег `{% url %}` по именам маршрутов из `urls.py` приложений                                                                                                          |
| 8  | Использование базового шаблона         | `templates/base.html`                                                                                                                                                                                                  | в нём общее: тип документа, `head`, Bootstrap, свой CSS, логотип, навигация, контейнер, подвал и подключение JS. Дублировать это в каждом шаблоне — значит править сайт в пяти местах вместо одного            |
| 9  | Наследование шаблонов                  | `links/templates/links/link_list.html:1`                                                                                                                                                                               | `{% extends "base.html" %}` связывает страницу с каркасом. Без наследования страница потеряет `head`, навигацию и подвал — останется только содержимое блоков                                                  |
| 10 | Использование блоков шаблона           | `templates/base.html:6`, `:25`; `link_list.html:3`, `:5`                                                                                                                                                               | дочерний шаблон переопределяет `title` и `content`; чтобы изменить заголовок одной страницы, правится только её блок                                                                                           |
| 11 | Передача контекста в шаблон            | `links/views.py:37–43`                                                                                                                                                                                                 | в контексте — список `cards`; шаблон обращается к ним по имени `cards`. Изменишь значение в контексте — изменится страница                                                                                     |
| 12 | Вывод значений в шаблоне               | `link_card.html:12,16,18`, `link_detail.html:28`                                                                                                                                                                       | `{{ card.link.url }}` и подобные выражения берут атрибуты объекта из контекста. В отличие от ПР5, HTML не склеивается в Python                                                                                 |
| 13 | Циклы в шаблонах                       | `link_list.html:10–14`, `click_list.html:11–15`                                                                                                                                                                        | перебирается коллекция из контекста; сколько записей в данных — столько и фрагментов HTML                                                                                                                      |
| 14 | Условия в шаблонах                     | `links/.../link_status.html:1`, `link_detail.html:12,42,51`                                                                                                                                                            | `{% if available %}` выбирает цвет бейджа, `{% if card %}` — карточку или сообщение об отсутствии. Альтернативная ветка — `{% else %}`                                                                         |
| 15 | Обработка пустой коллекции             | `link_list.html:12`, `click_list.html:13`                                                                                                                                                                              | `{% empty %}` внутри `{% for %}`: если список пуст, пользователь увидит «Ссылки не найдены»                                                                                                                    |
| 16 | Повторное использование фрагментов     | `base.html:22`, `link_list.html:11`, `link_card.html:8`, `link_detail.html:18`, `click_row.html:16`, `click_detail.html:25`                                                                                            | навигация, карточка ссылки и бейдж состояния вынесены в отдельные шаблоны. Бейдж подключается с параметрами `with state=... available=...` и используется на четырёх страницах                                 |
| 17 | Формирование ссылок `{% url %}`        | `navigation.html:2–4`, `link_card.html:4`, `click_row.html:2`                                                                                                                                                          | Django ищет маршрут по имени и подставляет адрес; идентификатор передаётся аргументом: `{% url 'links:detail' card.link.code %}`                                                                               |
| 18 | Пространства имён URL                  | `homepage/urls.py:7`, `links/urls.py:7`, `clicks/urls.py:7`                                                                                                                                                            | `app_name` даёт имена `homepage:index`, `links:list`, `links:detail`, `clicks:list`, `clicks:detail`. Если ссылка не разрешается — проверить `app_name`, `name=` в `path()` и `include()` в корневом `urls.py` |
| 19 | Фильтры шаблонов                       | `link_list.html:8` и `click_list.html:8` (`length`), `link_card.html:16` и `click_row.html:13` (`default`), `link_card.html:18` (`date`), `link_card.html:12` (`truncatechars`), `link_detail.html:49` (`floatformat`) | фильтр меняет представление значения: количество элементов, формат даты, обрезка длинного адреса, значение по умолчанию. Обычное `{{ ... }}` выводит значение как есть                                         |
| 20 | Подключение статических файлов         | `base.html:1` (`{% load static %}`), `:11`, `:16`, `:33`; каталог `homepage/static/homepage/`                                                                                                                          | путь строит тег `static`, поэтому он не зависит от настроек адресов и каталога статики                                                                                                                         |
| 21 | Анализ оформления страницы             | `homepage/static/homepage/css/style.css`                                                                                                                                                                               | классы `.service-logo`, `.service-nav`, `.link-card`, `.link-status`, `.click-source`, `.service-footer`. Без CSS останется только оформление Bootstrap; загрузку файла видно во вкладке Network               |
| 22 | Подключение JavaScript                 | `base.html:33`, `homepage/static/homepage/js/main.js`, `base.html:30`                                                                                                                                                  | скрипт подставляет текущий год в элемент `#current-year` в подвале. Проверить просто: год в подвале есть, а в HTML-шаблоне его нет                                                                             |
| 23 | Разделение логики и отображения        | `links/views.py:14–29` против `link_card.html`                                                                                                                                                                         | состояние ссылки считает Python: шаблоны Django не умеют вызывать методы с аргументами, а `get_state(today)` требует дату. Нужны другие данные — правится view, нужен другой вид — правится шаблон             |
| 24 | Отказ от формирования HTML в Python    | `git show "pr5:homepage/views.py"` против `homepage/views.py:7`                                                                                                                                                        | в ПР5 каркас собирала `page()`, теперь его нет: `grep -rn "page(" homepage links clicks --include="*.py"` ничего не находит. Разметка живёт в шаблонах, а view готовит данные                                  |
| 25 | Проверка целостности реализации        | путь `/links/mirea/`: `shortener/urls.py:11` → `links/urls.py:11` → `links/views.py:46` → `storage.py:141` → `links/views.py:14` → `link_detail.html` → `base.html` → статика                                          | если страница сломалась, проверяются именно эти файлы по порядку: маршрут, view, загрузка данных, контекст, шаблон, базовый шаблон, статика                                                                    |

## Чек-лист проекта (§7.2), 33 пункта

| № | Требование | Где это |
|---|---|---|
| 1 | Проект ПР1–ПР5 сохранён | `main.py`, `models/`, `storage.py`, `tests/`, `data/`; консоль работает |
| 2 | Структура `templates`, параметр `DIRS` | `templates/`, `shortener/settings.py:65` |
| 3 | Базовый шаблон | `templates/base.html` |
| 4 | `{% extends %}` | `index.html:1`, `not_found.html:1`, `link_list.html:1`, `link_detail.html:1`, `click_list.html:1`, `click_detail.html:1` |
| 5 | `{% block %}` | `base.html:6,25` и блоки дочерних шаблонов |
| 6 | `{% include %}` | `base.html:22`, `link_list.html:11`, `click_list.html:12`, `link_card.html:8` |
| 7 | Навигация в отдельном шаблоне | `templates/includes/navigation.html` |
| 8 | Шаблоны списка ссылок | `links/templates/links/link_list.html`, `includes/link_card.html` |
| 9 | Шаблон отдельной ссылки | `links/templates/links/link_detail.html` |
| 10 | Шаблоны списка переходов | `clicks/templates/clicks/click_list.html`, `includes/click_row.html` |
| 11 | Шаблон отдельного перехода | `clicks/templates/clicks/click_detail.html` |
| 12 | Данные через `context` | `links/views.py:37`, `clicks/views.py:28`, `links/views.py:56` |
| 13 | `{% for %}` | `link_list.html:10`, `click_list.html:11` |
| 14 | `{% if %}` | `link_status.html:1`, `link_detail.html:12`, `click_detail.html:12` |
| 15 | Обработка пустого списка | `link_list.html:12`, `click_list.html:13` |
| 16 | `app_name` | `homepage/urls.py:7`, `links/urls.py:7`, `clicks/urls.py:7` |
| 17 | Именованные URL | `name=` в `path()` всех трёх приложений |
| 18 | `{% url %}` | `navigation.html`, `link_card.html:4`, `click_row.html:2,8`, `link_detail.html:65` |
| 19 | Пространства имён | `links:list`, `links:detail`, `clicks:list`, `clicks:detail`, `homepage:index` |
| 20 | Фильтры шаблонов | `length`, `default`, `date`, `truncatechars`, `floatformat` — см. пункт 19 таблицы выше |
| 21 | Собственный CSS | `homepage/static/homepage/css/style.css`, подключение `base.html:11` |
| 22 | Изображение | `homepage/static/homepage/img/logo.png`, подключение `base.html:16` |
| 23 | JavaScript | `homepage/static/homepage/js/main.js`, подключение `base.html:33` |
| 24 | `page()` не используется | `grep -rn "page(" homepage links clicks --include="*.py"` — пусто |
| 25 | Все страницы работают | семь адресов из раздела «Перед защитой» |
| 26 | Данные из существующей модели объектов | `models/`, `storage.py:141`; страницы показывают `Link`, `Click`, `User` |
| 27 | JSON-хранилище сохранено | `data/users.json`, `data/links.json`, `data/clicks.json` |
| 28 | ORM не внедрялся преждевременно | `links/models.py`, `clicks/models.py`, `homepage/models.py` пустые (только docstring) |
| 29 | README.md обновлён | разделы «Шаблоны Django», «Структура проекта», «Текущее состояние» |
| 30 | `manage.py check` без ошибок | `System check identified no issues` |
| 31 | `pytest -v` выполнен | 28 тестов проходят |
| 32 | `flake8` выполнен | замечаний нет; дополнительно `ruff check` и `mypy` |
| 33 | Коммит работы | «ПР 6», тег `pr6` |

## Если спросят про отличие от ПР5

| | ПР5 | ПР6 |
|---|---|---|
| HTML | строки в Python, функция `page()` | шаблоны `.html` |
| Данные в страницу | подстановка в f-строку | контекст и `render()` |
| Ссылки | жёсткие адреса `/links/` | `{% url 'links:list' %}` |
| Повторяющиеся части | копирование каркаса | `extends` и `include` |
| Оформление | только Bootstrap по CDN | Bootstrap плюс свои CSS, JS и логотип |
