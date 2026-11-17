"""Допишите view-функции homepage, about и ice_cream без HTML-тегов.
Ответы: / — «Главная страница»; /about/ — «Описание проекта»;
/ice_cream/ — «Каталог мороженого»; /ice_cream/<номер>/ —
«Мороженое номер <номер>», где номер берётся из параметра pk.
"""

from django.http import HttpResponse


def ice_cream_detail(request, pk):
    return HttpResponse(f"Мороженое номер {pk}")


def ice_cream_list(request):
    return HttpResponse("Каталог мороженого")
