from rest_framework import serializers

from .models import Booking
from tours.serializers import TourSerializer


class BookingCreateSerializer(serializers.Serializer):
    tour = serializers.SlugField()
    count = serializers.IntegerField(min_value=1, max_value=20)


class BookingSerializer(serializers.ModelSerializer):
    tour = TourSerializer(read_only=True)
    tour_slug = serializers.CharField(
        source="tour.slug",
        read_only=True,
    )
    tour_title = serializers.CharField(
        source="tour.title",
        read_only=True,
    )

    class Meta:
        model = Booking
        fields = [
            "id",
            "reference",
            "tour",
            "tour_slug",
            "tour_title",
            "count",
            "unit_price",
            "total_price",
            "status",
            "payment_status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields