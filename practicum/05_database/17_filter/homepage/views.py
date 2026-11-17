"""
Используя метод `.filter()` передайте на главную страницу проекта названия и
описания только тех сортов мороженого, у которых установлен флаг
`is_published`.
"""

from django.shortcuts import render

from ice_cream.models import IceCream


def index(request):
    template = "homepage/index.html"
    # Добавьте фильтрацию по полю is_published.
    ice_cream_list = IceCream.objects.filter(is_published=True).values(
        "id", "title", "description"
    )
    context = {
        "ice_cream_list": ice_cream_list,
    }
    return render(request, template, context)
