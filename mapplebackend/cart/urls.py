from django.urls import path
from .views import CartView
from .item_views import CartItemView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('item/<int:item_id>/', CartItemView.as_view()),
]
