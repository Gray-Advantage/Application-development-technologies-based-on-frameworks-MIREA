"""Маршруты приложения links."""

from django.urls import path

from . import views

app_name = "links"

urlpatterns = [
    path("", views.links, name="list"),
    path("available/", views.available, name="available"),
    path("statistics/", views.stats, name="statistics"),
    path("manage/create/", views.link_create, name="create"),
    path("<slug:code>/", views.link_detail, name="detail"),
    path("<slug:code>/edit/", views.link_edit, name="edit"),
    path("<slug:code>/disable/", views.link_disable, name="disable"),
]
