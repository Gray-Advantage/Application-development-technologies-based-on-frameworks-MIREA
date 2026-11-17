"""Настройте корневой *urls.py*:

- все адреса вида *ice_cream/...* должны передаваться в *urls.py* приложения
**ice_cream**;

Создайте файл *urls.py* в приложении **ice_cream**. В нём настройте адреса
таким образом, чтобы:

- запросы к адресу *ice_cream/* обрабатывались view-функцией `ice_cream_list()`
из приложения **ice_cream**;
- запросы к адресам вида *ice_cream/1/*, *ice_cream/2/*, *ice_cream/42/* и к
прочим подобным — view-функцией `ice_cream_detail()` из приложения
**ice_cream**. В качестве переменной пути должны приниматься только
положительные целочисленные значения и ноль.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("homepage.urls")),
    path("about/", include("about.urls")),
    path("ice_cream/", include("ice_cream.urls")),
    path("admin/", admin.site.urls),
]
