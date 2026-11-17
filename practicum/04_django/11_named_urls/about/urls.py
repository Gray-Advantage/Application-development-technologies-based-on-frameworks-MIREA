"""Задайте namespace приложений homepage, about и ice_cream равным имени
приложения через app_name. Имена всех path должны совпадать с именами
view-функций. В includes/header.html и ice_cream/list.html замените
комментарии-заглушки ссылками через тег url с namespace и name.
Тексты: «Главная», «Список мороженого», «О проекте», «Подробнее».
В ссылку подробностей передавайте id соответствующего мороженого.
"""

from django.urls import path

from . import views

app_name = "about"

urlpatterns = [
    path("", views.description, name="description"),
]
