from django.urls import path
from .views import ProductReviewListView, ProductReviewView

urlpatterns = [
    path("products/<int:product_id>/reviews/", ProductReviewListView.as_view()),
    path("products/<int:product_id>/reviews/add/", ProductReviewView.as_view()),
]
