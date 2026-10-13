"""Маршруты приложения links."""

from django.urls import path

from . import views

app_name = "links"

urlpatterns = [
    path("", views.links, name="list"),
    path("<slug:code>/", views.link_detail, name="detail"),
]
