# ПР5: что показывать на защите

Проект: сервис сокращения ссылок. Коммит работы — «ПР 5», тег `pr5`.

> **Важно.** ПР6 переводит страницы на шаблоны и удаляет функцию `page()`.
> Поэтому пункты 11–15, 18, 19, 23 и 25 в текущем коде выглядят иначе.
> Для них указан и файл из коммита ПР5. Показать файл из истории:
>
> ```bash
> git show "pr5:homepage/views.py"
> ```
>
> Либо развернуть состояние ПР5 в отдельном каталоге и открыть его в IDE:
>
> ```bash
> git worktree add /tmp/pr5 pr5
> ```

## Перед защитой

```bash
python manage.py check
```

```bash
python manage.py runserver
```

Открыть в браузере: `/`, `/links/`, `/links/mirea/`, `/links/nosuchcode/`,
`/clicks/`, `/clicks/4/`, `/clicks/999/`.

## Таблица оценивания (§7.5), 25 показателей

| № | Показатель | Где смотреть | Что сказать |
|---|---|---|---|
| 1 | Структура проекта Django | `shortener/settings.py`, `shortener/urls.py` | `settings.py` — настройки проекта (приложения, шаблоны, БД, локализация), корневой `urls.py` — маршрутизация верхнего уровня |
| 2 | Проверка и запуск | `manage.py` | `manage.py check` проверяет конфигурацию, `manage.py runserver` запускает сервер разработки; сам файл — точка запуска команд управления |
| 3 | Регистрация приложений | `shortener/settings.py:38–47` | `homepage`, `links`, `clicks` в `INSTALLED_APPS`; без регистрации Django не найдёт шаблоны, статику и модели приложения |
| 4 | Структура приложений | `homepage/`, `links/`, `clicks/` | `homepage` — главная и общий каркас, `links` — ссылки, `clicks` — переходы. Для пользователей приложение не создавали: в Django есть `django.contrib.auth` с моделью `User` (`settings.py:40`) |
| 5 | Настройки режима отладки | `shortener/settings.py:31`, `:33` | перед выключением `DEBUG` заполнить `ALLOWED_HOSTS`, иначе Django ответит 400; при `DEBUG = False` видна своя страница 404, а статику сервер разработки не раздаёт |
| 6 | Маршрутизация между файлами URLconf | `shortener/urls.py:12` → `clicks/urls.py:11` → `clicks/views.py:33` | корневой файл обрабатывает префикс `clicks/` и через `include()` передаёт остаток адреса (`999/`) в маршруты приложения |
| 7 | Связь маршрута и view | `clicks/urls.py:11` | `path("<int:click_id>/", views.click_detail, name="detail")`: значение из адреса приходит в параметр `click_id`. При переименовании view правится только `urls.py`; `name=` позволяет строить ссылки по имени, а не по адресу |
| 8 | Работа конвертера URL | `clicks/urls.py:11`, `links/urls.py:11` | `/clicks/abc/` не дойдёт до view: конвертер `<int:...>` не принимает буквы, Django не находит маршрут. `/clicks/999/` дойдёт, а 404 вернёт уже сама view. У ссылок конвертер `<slug:code>`, поэтому `/links/mirea/` работает |
| 9 | Обработка HTTP-запроса | `shortener/urls.py:10` → `homepage/urls.py:10` → `homepage/views.py:7` | адрес `/` доходит до `index()`, функция формирует страницу, Django возвращает `HttpResponse` браузеру |
| 10 | Взаимодействие запроса и представления | `homepage/views.py:7`; ПР5: `homepage/views.py:47` | первый параметр view — `request`, возвращается `HttpResponse`. Если вернуть обычную строку, Django выдаст ошибку: view не вернула объект ответа |
| 11 | Формирование HTML-страницы | ПР5: `homepage/views.py:38` → `:11` → `:47` | в `index()` формируется `content`, он передаётся в `page()`, та собирает документ, результат уходит в `HttpResponse` |
| 12 | Назначение функции `page()` | ПР5: `homepage/views.py:11–33` | общий каркас: кодировка, `viewport`, `title`, подключение Bootstrap, навигация, `container`. Каждая view передаёт только заголовок и содержимое |
| 13 | Повторное использование HTML | ПР5: `links/views.py:38`, `clicks/views.py:29` | каркас формирует `page()`, содержимое — конкретная view; одна функция обслуживает все страницы |
| 14 | Изменение содержимого страницы | ПР5: `clicks/views.py:29` | поменять первый аргумент `page()` — изменится только заголовок вкладки, каркас останется прежним |
| 15 | Подключение Bootstrap | ПР5: `homepage/views.py:5`, `:23` | CSS подключён по CDN; классы `nav`, `container`, `list-group`, `card`, `badge`, `btn`, `display-4`, `lead`. Без подключения останется голый HTML без оформления |
| 16 | Загрузка и поиск данных | `storage.py:141`, `models/links.py:117`, `models/clicks.py:69` | `load_all()` возвращает три коллекции объектов, `find_link_by_code()` и `find_click_by_id()` — объект или `None` |
| 17 | Путь данных от JSON до представления | `data/links.json` → `storage.py:19` → `storage.py:66` → `storage.py:141` → `links/views.py:48` | запись читается из файла, `link_from_data()` находит владельца по `owner_id` и создаёт объект `Link`, `load_all()` собирает коллекции, view получает готовые объекты |
| 18 | Использование объекта в представлении | `links/views.py:46–55`; ПР5: `links/views.py:64` | view берёт объект у функции поиска и обращается к его атрибутам: `link.short_url`, `link.url`, `link.owner.username` |
| 19 | Преобразование атрибутов в HTML | ПР5: `links/views.py:64–96` | атрибуты подставляются в f-строку. Если поправить `data/links.json`, изменится и страница |
| 20 | Типы данных | `models/links.py:33–48`, `models/clicks.py:20–31` | `code` и `url` — строки, `created_at` и `expires_at` — `date`, `is_active` — `bool`, `owner` — объект `User`, `click.id` — `int` |
| 21 | Обработка ошибки 404 | `shortener/urls.py:6`, `homepage/views.py:12` | `handler404` объявлен в корневом `urls.py` и указывает на `page_not_found()`; функция возвращает ответ со статусом 404 и работает при `DEBUG = False` |
| 22 | Ошибка маршрутизации и отсутствие ресурса | `/nosuchpage/` против `/links/nosuchcode/` | в первом случае маршрут не найден и срабатывает `handler404`; во втором маршрут есть, но объекта нет — 404 возвращает сама view |
| 23 | Ветвление в представлении | `links/views.py:51`; ПР5: `links/views.py:45` | проверка `if link is None`. Без неё обращение к атрибуту `None` упадёт с `AttributeError` |
| 24 | Обработка отсутствующего объекта | `models/links.py:117` | функция поиска возвращает `None`, поэтому результат проверяют до обращения к атрибутам |
| 25 | Изменение HTTP-статуса | `links/views.py:61`; ПР5: `links/views.py:55` | заменить `404` на `403`; проверить `curl -I http://127.0.0.1:8000/links/nosuchcode/`. 404 означает «нет ресурса», 403 — «доступ запрещён» |

## Чек-лист проекта (§7.2), 19 пунктов

| № | Требование | Где это |
|---|---|---|
| 1 | Проект ПР3 сохранён и продолжен | `main.py`, `models/`, `tests/`, `data/` на месте; `python main.py` работает |
| 2 | Создан Django-проект | `manage.py`, `shortener/` |
| 3 | Созданы Django-приложения | `homepage/`, `links/`, `clicks/` |
| 4 | Приложения подключены к проекту | `shortener/settings.py:45–47` |
| 5 | Настроена маршрутизация | `shortener/urls.py:8–13`, `homepage/urls.py`, `links/urls.py`, `clicks/urls.py` |
| 6 | Настроена обработка ошибки 404 | `shortener/urls.py:6`, `homepage/views.py:12` |
| 7 | Реализованы view-функции | `homepage/views.py:7`, `links/views.py:31,46`, `clicks/views.py:22,33` |
| 8 | Создана главная страница | `/` → `homepage/views.py:7` |
| 9 | Созданы страницы предметной области | `/links/`, `/links/<code>/`, `/clicks/`, `/clicks/<id>/` |
| 10 | Используются динамические URL | `links/urls.py:11` (`<slug:code>`), `clicks/urls.py:11` (`<int:click_id>`) |
| 11 | Организована навигация | `templates/includes/navigation.html`; ПР5: `homepage/views.py:26` |
| 12 | Используется HTML | шаблоны в `templates/`; ПР5: HTML в `homepage/views.py:11` |
| 13 | Используется CSS и Bootstrap | `templates/base.html:9–11`, `homepage/static/homepage/css/style.css` |
| 14 | Сохраняется предметная область | `models/`, `storage.py`; страницы показывают `Link`, `Click`, `User` |
| 15 | Приложение запускается без ошибок | `python manage.py check`, `python manage.py runserver` |
| 16 | Реализованные URL проверены | все семь адресов из раздела «Перед защитой» |
| 17 | README.md обновлён | разделы «Используемые технологии», «Веб-интерфейс», «Структура проекта» |
| 18 | Код проверен | `flake8`, `ruff check`, `mypy`, `pytest -v` (28 тестов) |
| 19 | Результат зафиксирован в Git | коммит «ПР 5», тег `pr5` |
