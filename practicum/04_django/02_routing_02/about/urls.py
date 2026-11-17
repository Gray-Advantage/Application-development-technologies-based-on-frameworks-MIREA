"""Подключите страницу about/ к функции about.views.description().

В приложении about создайте urls.py, импортируйте path и views.
В urlpatterns объявите пустой маршрут к функции description():
префикс about/ задаётся при подключении в корневом urls.py проекта.
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.description),
]
