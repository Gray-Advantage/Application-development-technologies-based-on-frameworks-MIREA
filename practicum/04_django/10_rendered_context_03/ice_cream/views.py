"""На страницу со списком мороженого выведите данные обо всех сортах. Должна
получиться такая страница:

![](https://pictures.s3.yandex.net:443/resources/S01_123_1677516225.png)

**Что надо сделать**

Доработайте view-функцию `ice_cream_list()`:

- передайте в словарь `context` список словарей `ice_cream_catalog`;
- словарь `context` передайте в шаблон.

В шаблоне *templates/ice_cream/list.html*:

Перечень сортов мороженого должен быть заключён в маркированный HTML-список.

- Переберите сорта мороженого в цикле `{% for ... in ... %}`;
- в цикле оберните каждый сорт в тег `<li>`;
- у каждого сорта выведите значения:
    - `title` — как заголовок третьего уровня `<h3>`;
    - `description` — как текстовый абзац `<p>`;
- после каждого элемента списка, кроме последнего, должна быть горизонтальная
линия `<hr>`.

В шаблоне вам нужно написать примерно такой код:

```html
<ul>
  {% Переберите элементы списка for  %}
    <li>
      <h3>{{ title сорта }}</h3>
      <p>{{ description сорта }}</p>
    </li>
    {% if проверка, что итерация не последняя %}
      <hr>
    {% endif %}
 {% endfor %}
</ul>
```
"""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

ice_cream_catalog = [
    {
        "id": 0,
        "title": "Классический пломбир",
        "description": "Настоящее мороженое, "
        "для истинных ценителей вкуса. "
        "Если на столе появляется пломбир"
        " — это не надолго.",
    },
    {
        "id": 1,
        "title": "Мороженое с кузнечиками",
        "description": "В колумбийском стиле: мороженое "
        "с добавлением настоящих карамелизованных кузнечиков.",
    },
    {
        "id": 2,
        "title": "Мороженое со вкусом сыра чеддер",
        "description": "Вкус настоящего сыра в вафельном стаканчике.",
    },
]


def ice_cream_detail(request: HttpRequest, pk: int) -> HttpResponse:
    template = "ice_cream/detail.html"
    context = {"ice_cream": ice_cream_catalog[pk]}
    return render(request, template, context)


def ice_cream_list(request: HttpRequest) -> HttpResponse:
    template = "ice_cream/list.html"
    context = {"ice_cream_catalog": ice_cream_catalog}
    return render(request, template, context)
