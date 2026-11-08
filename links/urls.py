"""Маршруты приложения links."""

from django.urls import path

from . import views

app_name = "links"

urlpatterns = [
    path("", views.links, name="list"),
    path("available/", views.available, name="available"),
    path("statistics/", views.stats, name="statistics"),
    path("<slug:code>/", views.link_detail, name="detail"),
]
