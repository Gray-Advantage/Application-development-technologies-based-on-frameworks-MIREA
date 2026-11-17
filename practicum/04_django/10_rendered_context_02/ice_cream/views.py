"""В файле *ice_cream/views.py* создан список словарей `ice_cream_catalog`.

Допишите view-функцию `ice_cream_detail()` так, чтобы при запросах
*ice_cream/0/*, *ice_cream/1/* и *ice_cream/2/* она извлекала информацию из
элемента списка с соответствующим индексом и передавала их в шаблон. Список
должен содержать один элемент: `{<название_ключа>: <элемент_списка>}`.

В результате должна вернуться такая страница (на примере запроса
*ice_cream/0/*):

![](https://pictures.s3.yandex.net:443/resources/S01_122_1676930218.png)

На остальных запросах проект будет падать с исключением `list index out of
range`; пусть так и будет, не страшно.
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
    return render(request, template)
