"""Маршруты приложения clicks."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.clicks, name="clicks"),
    path("<int:click_id>/", views.click_detail, name="click_detail"),
]
