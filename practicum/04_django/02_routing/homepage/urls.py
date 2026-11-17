"""Настройте anfisa_for_friends/urls.py и homepage/urls.py так, чтобы
запрос к главной странице обрабатывала функция homepage.views.index().
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
]
