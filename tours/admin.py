from django.contrib import admin

from .models import Tour


class ItineraryInlineNote(admin.ModelAdmin):
    list_display = (
        "title",
        "city",
        "category",
        "price",
        "seats_available",
        "is_active",
        "is_featured",
    )
    list_filter = ("category", "is_active", "is_featured")
    search_fields = ("title", "city", "slug")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("price", "is_active", "is_featured")
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Tour, ItineraryInlineNote)