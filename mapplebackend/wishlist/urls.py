from django.urls import path
from .views import WishlistView, WishlistItemDeleteView

urlpatterns = [
    path('', WishlistView.as_view()),
    path('item/<int:pk>/', WishlistItemDeleteView.as_view())
]

