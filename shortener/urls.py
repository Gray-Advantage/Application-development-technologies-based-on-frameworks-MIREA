"""Корневая маршрутизация проекта: адреса распределены по приложениям."""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

handler404 = "homepage.views.page_not_found"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("links/", include("links.urls")),
    path("clicks/", include("clicks.urls")),
]

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
