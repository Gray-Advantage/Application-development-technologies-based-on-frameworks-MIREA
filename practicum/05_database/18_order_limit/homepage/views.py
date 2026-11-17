"""
В проекте «Анфиса для друзей» отредактируйте view-функцию `index()` в
*homepage/views.py* таким образом, чтобы на главную страницу выводились
значения полей

- id
- title
- description

Запрос должен вернуть первые **три** сорта мороженого, у которых значение полей
`is_published` и `is_on_main` равно `True`. Записи должны быть отсортированы по
полю `title` в алфавитном порядке.

HTML-шаблон для вывода данных на страницу уже подготовлен; ваша задача — только
дописать view-функцию.
"""

from django.shortcuts import render

from ice_cream.models import IceCream


def index(request):
    template = "homepage/index.html"
    # Нужно вывести три сорта мороженого отсортированные по title по алфавиту,
    # у которых значение полей is_published и is_on_main равно True.
    ice_cream_list = (
        IceCream.objects.filter(is_published=True, is_on_main=True)
        .values("id", "title", "description")
        .order_by("title")[:3]
    )
    context = {
        "ice_cream_list": ice_cream_list,
    }
    return render(request, template, context)
