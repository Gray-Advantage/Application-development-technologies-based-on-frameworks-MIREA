"""Административный интерфейс журнала переходов."""

from django.contrib import admin

from .models import Click


@admin.register(Click)
class ClickAdmin(admin.ModelAdmin):
    list_display = ("id", "link", "owner", "clicked_at", "source")
    search_fields = ("link__code", "link__owner__username", "source")
    list_filter = ("clicked_at", "link__status")
    list_select_related = ("link__owner",)
    ordering = ("-clicked_at", "-pk")
    date_hierarchy = "clicked_at"
    list_per_page = 10
    autocomplete_fields = ("link",)

    @admin.display(description="Владелец", ordering="link__owner__username")
    def owner(self, obj: Click) -> str:
        return obj.link.owner.username
