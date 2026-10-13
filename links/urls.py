"""Маршруты приложения links."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.links, name="links"),
    path("<slug:code>/", views.link_detail, name="link_detail"),
]
