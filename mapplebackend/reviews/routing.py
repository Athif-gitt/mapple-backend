from django.urls import path
from reviews.consumers import ReviewConsumer

websocket_urlpatterns = [
    path(
        "ws/products/<int:product_id>/reviews/",
        ReviewConsumer.as_asgi(),
    ),
]
