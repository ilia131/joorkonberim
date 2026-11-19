from rest_framework import serializers

from .models import Tour


def _seo_excerpt(value, limit=155):
    """Return a plain-text excerpt without cutting the final word."""
    import re

    text = re.sub(r"<[^>]*>", " ", value or "")
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    excerpt = text[: limit + 1].rsplit(" ", 1)[0].strip()
    return (excerpt or text[:limit]).rstrip(" ،؛,.") + "…"


class TourSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    seo_title = serializers.SerializerMethodField()
    seo_description = serializers.SerializerMethodField()
    image_alt = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = [
            "id", "slug", "title", "city", "category",
            "duration", "date", "price", "old_price", "rating",
            "reviews", "seats_total", "seats_available", "image",
            "badge", "description", "includes", "itinerary",
            "is_active", "is_featured", "created_at", "updated_at",
            "seo_title", "seo_description", "image_alt",
        ]

    def get_image(self, obj):
        if not obj.image:
            return None
        request = self.context.get("request")
        image_url = obj.image.url
        return request.build_absolute_uri(image_url) if request else image_url

    def get_seo_title(self, obj):
        # Provide a fallback for the frontend; real page titles must be
        # rendered in the initial HTML, not added only after hydration.
        return f"{obj.title} | تور {obj.city} | جور کن بریم"[:65]

    def get_seo_description(self, obj):
        introduction = f"{obj.title} در {obj.city}. "
        return _seo_excerpt(introduction + obj.description)

    def get_image_alt(self, obj):
        return f"تصویر تور {obj.title} در {obj.city}"
