"""Подключите страницу about/ к функции about.views.description().

Создайте about/urls.py с импортами path и views, объявите urlpatterns
с маршрутом к description(). В корневом anfisa_for_friends/urls.py
подключите маршруты приложения about с префиксом about/ через include.
Сохраните существующие маршруты главной страницы и административного сайта.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("homepage.urls")),
    path("about/", include("about.urls")),
    path("admin/", admin.site.urls),
]
