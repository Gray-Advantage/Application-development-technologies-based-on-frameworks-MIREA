"""
На главную страницу проекта выводятся описания сортов мороженого.

Дополните view-функцию `index()` в файле *homepage/views.py*: для каждого сорта
мороженого выведите название связанной с ним обёртки (объекта `Wrapper`). Во
view-функции `index()` получите нужную информацию из БД, передайте её в шаблон
и выведите в строке, отмеченной комментарием.

Не удаляйте фильтры `is_on_main=True, is_published=True` и сортировку для
модели `IceCream`.

Решить задачу можно двумя способами.
"""

from django.shortcuts import render

from ice_cream.models import IceCream


def index(request):
    template = "homepage/index.html"
    # Доработайте запрос.
    ice_cream_list = (
        IceCream.objects.filter(is_on_main=True, is_published=True)
        .order_by("title")
        .values("id", "title", "description", "wrapper__title")
    )
    context = {
        "ice_cream_list": ice_cream_list,
    }
    return render(request, template, context)
