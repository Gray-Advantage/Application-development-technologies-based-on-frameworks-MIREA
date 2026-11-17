"""
В файле *homepage/views.py* измените функцию `index()` так, чтобы на главную
страницу проекта передавались только те данные, которые используются в шаблоне.
"""

from django.shortcuts import render

from ice_cream.models import IceCream


def index(request):
    template = "homepage/index.html"
    # Запишите в переменную ice_cream_list новый QuerySet
    ice_cream_list = IceCream.objects.values("id", "title", "description")
    context = {
        "ice_cream_list": ice_cream_list,
    }
    return render(request, template, context)
