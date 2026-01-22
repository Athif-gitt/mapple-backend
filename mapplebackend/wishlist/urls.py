from django.urls import path
from .views import WishlistView, WishlistItemDeleteView

urlpatterns = [
    path('', WishlistView.as_view()),
    path('item/<int:product_id>/', WishlistItemDeleteView.as_view())
]

