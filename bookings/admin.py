from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "user",
        "tour",
        "count",
        "total_price",
        "status",
        "payment_status",
        "created_at",
    )

    list_filter = ("status", "payment_status", "created_at")
    search_fields = (
        "reference",
        "user__email",
        "tour__title",
    )

    readonly_fields = (
        "reference",
        "user",
        "tour",
        "count",
        "unit_price",
        "total_price",
        "created_at",
        "updated_at",
    )