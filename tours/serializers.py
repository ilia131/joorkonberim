from rest_framework import serializers

from .models import Tour





class TourSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = [
            "id",
            "slug",
            "title",
            "city",
            "category",
            "duration",
            "date",
            "price",
            "old_price",
            "rating",
            "reviews",
            "seats_total",
            "seats_available",
            "image",
            "badge",
            "description",
            "includes",
            "itinerary",
            "is_active",
            "is_featured",
            "created_at",
            "updated_at",
        ]

    def get_image(self, obj):
        if not obj.image:
            return None

        request = self.context.get("request")
        image_url = obj.image.url

        if request:
            return request.build_absolute_uri(image_url)

        return image_url
