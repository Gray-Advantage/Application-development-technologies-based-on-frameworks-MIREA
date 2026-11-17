"""Настройте anfisa_for_friends/urls.py и homepage/urls.py так, чтобы
запрос к главной странице обрабатывала функция homepage.views.index().
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("homepage.urls")),
    path("admin/", admin.site.urls),
]
