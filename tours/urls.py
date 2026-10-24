from django.urls import path

from .views import (
    TourListView,
    TourDetailView,
    TourCategoriesView,
    TourSearchView,
)

urlpatterns = [
    path("", TourListView.as_view(), name="tour-list"),
    path("categories/", TourCategoriesView.as_view(), name="tour-categories"),
    path("search/", TourSearchView.as_view(), name="tour-search"),
    path("<slug:slug>/", TourDetailView.as_view(), name="tour-detail"),
]