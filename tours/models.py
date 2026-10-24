from django.db import models
from django.utils.text import slugify


class Tour(models.Model):
    class Category(models.TextChoices):
        NATURE = "nature", "طبیعت‌گردی"
        DESERT = "desert", "کویر"
        SEA = "sea", "دریایی"
        CULTURAL = "cultural", "فرهنگی"
        ADVENTURE = "adventure", "ماجراجویی"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)

    city = models.CharField(max_length=100)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        db_index=True,
    )

    description = models.TextField()
    duration = models.CharField(max_length=100)
    date = models.CharField(max_length=100)

    price = models.PositiveBigIntegerField()
    old_price = models.PositiveBigIntegerField(
        null=True,
        blank=True,
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
    )
    reviews = models.PositiveIntegerField(default=0)

    seats_total = models.PositiveIntegerField(default=0)
    seats_available = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    # آپلود تصویر در پوشه media/tours/
    image = models.ImageField(
        upload_to="tours/",
        blank=True,
        null=True,
    )

    badge = models.CharField(max_length=80, blank=True)

    includes = models.JSONField(default=list, blank=True)
    itinerary = models.JSONField(default=list, blank=True)

    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_featured", "-created_at"]
        indexes = [
            models.Index(fields=["is_active", "category"]),
            models.Index(fields=["is_active", "price"]),
        ]

    def save(self, *args, **kwargs):
        if self.seats_available is None:
            self.seats_available = self.seats_total

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
