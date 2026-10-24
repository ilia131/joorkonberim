from django.db.models import Q
from rest_framework import generics, permissions, filters
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Tour
from .serializers import TourSerializer


CATEGORY_MAP = {
    "طبیعت‌گردی": "nature",
    "کویر": "desert",
    "دریایی": "sea",
    "فرهنگی": "cultural",
    "ماجراجویی": "adventure",
}


class TourListView(generics.ListAPIView):
    serializer_class = TourSerializer
    permission_classes = [permissions.AllowAny]

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["price", "rating", "created_at"]
    ordering = ["-is_featured", "-created_at"]

    def get_queryset(self):
        params = self.request.query_params
        queryset = Tour.objects.filter(is_active=True)

        category = params.get("category")
        if category and category != "همه تورها":
            category = CATEGORY_MAP.get(category, category)
            queryset = queryset.filter(category=category)

        query = params.get("q", params.get("search", "")).strip()
        if len(query) > 150:
            raise ValidationError({
                "q": "عبارت جستجو بیش از حد طولانی است."
            })

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(city__icontains=query)
                | Q(description__icontains=query)
                | Q(slug__icontains=query)
            )

        if params.get("featured") == "true":
            queryset = queryset.filter(is_featured=True)

        if params.get("available") == "true":
            queryset = queryset.filter(seats_available__gt=0)

        return queryset


class TourDetailView(generics.RetrieveAPIView):
    serializer_class = TourSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Tour.objects.filter(is_active=True)
    lookup_field = "slug"


class TourCategoriesView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response([
            {"value": value, "label": label}
            for value, label in Tour.Category.choices
        ])


class TourSearchView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        query = request.query_params.get("q", "").strip()

        if len(query) > 150:
            raise ValidationError({
                "q": "عبارت جستجو بیش از حد طولانی است."
            })

        queryset = Tour.objects.filter(is_active=True)

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(city__icontains=query)
                | Q(description__icontains=query)
                | Q(slug__icontains=query)
            )

        return Response(
            TourSerializer(queryset[:20], many=True).data
        )