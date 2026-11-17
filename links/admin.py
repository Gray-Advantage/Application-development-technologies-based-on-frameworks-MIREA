"""Административный интерфейс коротких ссылок."""

from django.contrib import admin
from django.http import HttpRequest

from clicks.models import Click

from .models import Link, LinkQuerySet


class ClickInline(admin.TabularInline):
    model = Click
    fields = ("clicked_at", "source")
    ordering = ("-clicked_at", "-pk")
    extra = 0
    show_change_link = True


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("code", "owner", "created_at", "expires_at", "status")
    list_display_links = ("code",)
    list_editable = ("status",)
    list_filter = ("status", "created_at", "expires_at")
    search_fields = ("code", "url", "owner__username")
    ordering = ("-created_at", "code")
    list_per_page = 10
    list_select_related = ("owner",)
    autocomplete_fields = ("owner",)
    inlines = (ClickInline,)
    actions = ("disable_links",)

    def get_readonly_fields(
        self, request: HttpRequest, obj: Link | None = None
    ) -> tuple[str, ...]:
        return ("code",) if obj is not None else ()

    @admin.action(
        description="Отключить выбранные ссылки", permissions=["change"]
    )
    def disable_links(
        self, request: HttpRequest, queryset: LinkQuerySet
    ) -> None:
        count = queryset.enabled().update(status=Link.Status.DISABLED)
        self.message_user(request, f"Отключено ссылок: {count}.")
