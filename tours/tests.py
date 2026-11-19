from django.test import TestCase
from rest_framework.test import APIRequestFactory

from .models import Tour
from .serializers import TourSerializer


class TourSEOMetadataTests(TestCase):
    def setUp(self):
        self.tour = Tour.objects.create(
            title="گردش یک‌روزه اصفهان",
            slug="isfahan-day-trip",
            city="اصفهان",
            category=Tour.Category.CULTURAL,
            description="<p>بازدید از میدان نقش جهان و بازار قیصریه</p>",
            duration="یک روز",
            date="به‌زودی",
            price=800000,
        )

    def test_metadata_is_in_tour_api_payload(self):
        request = APIRequestFactory().get("/api/tours/isfahan-day-trip/")
        data = TourSerializer(self.tour, context={"request": request}).data
        self.assertIn("جور کن بریم", data["seo_title"])
        self.assertIn("میدان نقش جهان", data["seo_description"])
        self.assertNotIn("<p>", data["seo_description"])
        self.assertIn("اصفهان", data["image_alt"])

    def test_description_is_bounded(self):
        self.tour.description = "سفر تاریخی و بازدید از جاذبه‌های شهر " * 30
        result = TourSerializer(self.tour).data["seo_description"]
        self.assertLessEqual(len(result), 156)
        self.assertTrue(result.endswith("…"))
