"""В проекте шаблоны находятся в общей директории templates.
Настройте view-функции приложений about, homepage и ice_cream:
возвращайте render() с шаблонами about/description.html,
homepage/index.html, ice_cream/detail.html и ice_cream/list.html
соответственно. В ice_cream_detail(request, pk) примите pk,
но передавать его в шаблон в этом задании не нужно.
"""

from django.shortcuts import render


def ice_cream_detail(request, pk):
    return render(request, "ice_cream/detail.html")


def ice_cream_list(request):
    return render(request, "ice_cream/list.html")
