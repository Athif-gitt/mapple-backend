from django.urls import path
from .views import CreateOrderView, VerifyPaymentView, OrderDetailView, OrderListView

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('create/', CreateOrderView.as_view(), name='create-order'),
    path('verify/', VerifyPaymentView.as_view(), name='verify-payment'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]
