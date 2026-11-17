# ПР11. Формы Django

Для демонстрации войдите через `/admin/login/` и откройте `/links/`.
Тестовые записи из ПР9 загружаются командой `python manage.py import_legacy`
один раз после миграций на чистой базе. Используйте суперпользователя либо
staff-аккаунт с разрешениями `links.add_link`, `links.change_link`.

## Пункты защиты 7.3

| № | Что показать |
| --- | --- |
| 1 | [ClickFilterForm](../clicks/forms.py). Классы полей и допустимые значения. |
| 2 | [clicks](../clicks/views.py) передаёт `request.GET` в форму, затем строит QuerySet из проверенных данных. |
| 3 | `/clicks/?date=abc` — ошибка даты и пустой список. Для сравнения `/clicks/?date=2026-09-02`. |
| 4 | [LinkForm.Meta](../links/forms.py) привязывает форму к Link и перечисляет разрешённые поля. |
| 5 | [Поле срока и DateInput](../links/forms.py), подписи из [модели](../links/models.py). |
| 6 | [link_create](../links/views.py). GET показывает форму. POST привязывает параметры и файл. |
| 7 | [clean_url, clean_code и clean](../links/forms.py). Показать ошибку срока или зарезервированного кода. |
| 8 | При создании повторить код `mirea`. Форма сообщит, что код занят. Уникальность также гарантирует [первичный ключ](../links/models.py). |
| 9 | [Общий шаблон полей](../templates/includes/form_fields.html) выводит подсказки, ошибки полей и общие ошибки отдельно. |
| 10 | [Сохранение](../links/views.py) через `form.save(commit=False)`, вставка с `force_insert`, перенаправление на карточку. |
| 11 | [link_edit](../links/views.py) передаёт `instance=link`. Изменить URL и показать неизменный адрес карточки. |
| 12 | [LinkForm](../links/forms.py) исключает изменение кода при редактировании и заново проверяет срок. |
| 13 | [link_disable](../links/views.py) вызывает [deactivate](../links/models.py). Ссылка исчезает из поиска, переходы сохраняются. |
| 14 | [POST-форма и CSRF-токен](../links/templates/links/link_detail.html), [require_POST](../links/views.py). |
| 15 | `/links/missing/edit/` или `/links/missing/` — 404. [Именованные маршруты](../links/urls.py). |
| 16 | [link_form.html](../links/templates/links/link_form.html) использует `multipart/form-data`. [Миграция](../links/migrations/0003_link_preview.py) добавляет ImageField. |
| 17 | [Прежний тест фильтров, сортировки и пагинации](../clicks/tests.py). `/clicks/?owner=2&code=mirea&sort=-date&page=2`. |
| 18 | Заменить или очистить изображение через редактирование, проверить [карточку и URL изображения](../links/templates/links/link_detail.html). |
| 19 | [Тесты формы и файлов](../links/test_forms.py). Неверный URL, отсутствующий владелец, неверный срок и файл с ложным PNG. |
| 20 | [Декораторы](../links/views.py), [тест доступа и CSRF](../links/test_forms.py). Гость перенаправляется на вход, аккаунт без права получает 403. |

## Чек-лист 7.2

| Пункты | Где проверить |
| --- | --- |
| 1–4 | [Форма фильтра](../clicks/forms.py), [обработка GET](../clicks/views.py), [тесты](../clicks/tests.py). |
| 5–7 | [ModelForm](../links/forms.py), [link_create](../links/views.py), [шаблон](../links/templates/links/link_form.html). |
| 8–10 | [Проверка срока, URL и кода](../links/forms.py), [ошибки](../templates/includes/form_fields.html). |
| 11–12 | [link_edit](../links/views.py) сохраняет тот же объект. Код исключён из редактируемых полей. |
| 13–14 | [link_disable](../links/views.py), [LinkQuerySet.available_on](../links/models.py). |
| 15–16 | [404 и POST с CSRF](../links/views.py), [форма отключения](../links/templates/links/link_detail.html). |
| 17 | [ImageField](../links/models.py), [медиа](../shortener/urls.py), [preview](../links/templates/links/link_detail.html). |
| 18 | [README](../README.md). |
| 19 | [Тесты сценариев](../links/test_forms.py), `python manage.py check`, `pytest -v`. |
| 20 | `git log --oneline --grep='^PR11:'`. |
