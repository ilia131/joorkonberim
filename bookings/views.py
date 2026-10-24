from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from tours.models import Tour

from .models import Booking
from .serializers import BookingCreateSerializer, BookingSerializer


class BookingListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Booking.objects
            .filter(user=self.request.user)
            .select_related("tour")
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BookingCreateSerializer
        return BookingSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        input_serializer = BookingCreateSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        slug = input_serializer.validated_data["tour"]
        count = input_serializer.validated_data["count"]

        tour = get_object_or_404(
            Tour.objects.select_for_update(),
            slug=slug,
            is_active=True,
        )

        if tour.seats_available is None or tour.seats_available < count:
            raise ValidationError({
                "count": "ظرفیت کافی برای این تعداد مسافر وجود ندارد."
            })

        if count > tour.seats_total:
            raise ValidationError({
                "count": "تعداد مسافران از ظرفیت کل تور بیشتر است."
            })

        # قیمت را از دیتابیس می‌گیریم، نه از درخواست فرانت‌اند.
        unit_price = tour.price
        total_price = unit_price * count

        tour.seats_available -= count
        tour.save(update_fields=["seats_available", "updated_at"])

        booking = Booking.objects.create(
            user=request.user,
            tour=tour,
            count=count,
            unit_price=unit_price,
            total_price=total_price,
            status=Booking.Status.PENDING,
            payment_status=Booking.PaymentStatus.UNPAID,
        )

        output_serializer = BookingSerializer(booking)
        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class BookingDetailView(generics.RetrieveAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "reference"

    def get_queryset(self):
        return Booking.objects.filter(
            user=self.request.user
        ).select_related("tour")


class BookingCancelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request, reference):
        booking = get_object_or_404(
            Booking.objects.select_for_update().select_related("tour"),
            reference=reference,
            user=request.user,
        )

        if booking.status != Booking.Status.PENDING:
            raise ValidationError({
                "status": "فقط رزروهای در انتظار پرداخت قابل لغو هستند."
            })

        if booking.payment_status != Booking.PaymentStatus.UNPAID:
            raise ValidationError({
                "payment_status": "این رزرو نیازمند بررسی وضعیت پرداخت است."
            })

        tour = Tour.objects.select_for_update().get(pk=booking.tour_id)

        booking.status = Booking.Status.CANCELLED
        booking.save(update_fields=["status", "updated_at"])

        Tour.objects.filter(pk=tour.pk).update(
            seats_available=F("seats_available") + booking.count
        )

        booking.refresh_from_db()
        return Response(BookingSerializer(booking).data)