"""Маршруты приложения clicks."""

from django.urls import path

from . import views

app_name = "clicks"

urlpatterns = [
    path("", views.clicks, name="list"),
    path("<int:click_id>/", views.click_detail, name="detail"),
]
