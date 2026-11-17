"""Административный интерфейс владельцев ссылок."""

from django.contrib import admin
from django.http import HttpRequest

from links.models import Link

from .models import User


class LinkInline(admin.TabularInline):
    model = Link
    fields = ("code", "url", "status")
    readonly_fields = fields
    extra = 0
    can_delete = False
    show_change_link = True

    def has_add_permission(
        self, request: HttpRequest, obj: User | None = None
    ) -> bool:
        return False


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "registered_at")
    search_fields = ("username", "email")
    list_filter = ("registered_at",)
    ordering = ("username",)
    list_per_page = 10
    inlines = (LinkInline,)
