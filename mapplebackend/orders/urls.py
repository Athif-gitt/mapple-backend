from django.urls import path
from .views import CreateOrderView, VerifyPaymentView, OrderDetailView, OrderListView, AdminStatsViews, AdminOrderListView, AdminOrderDetailView, AdminOrderStatusUpdateView

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('create/', CreateOrderView.as_view(), name='create-order'),
    path('verify/', VerifyPaymentView.as_view(), name='verify-payment'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('admin/stats/', AdminStatsViews.as_view()),
    path('admin/orders/', AdminOrderListView.as_view(), name='admin-orders'),
    path('admin/orders/<int:pk>/', AdminOrderDetailView.as_view(), name='admin-order-detail'),
    path('admin/orders/<int:pk>/status/', AdminOrderStatusUpdateView.as_view(), name='admin-order-status'),
]
