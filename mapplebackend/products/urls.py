from django.urls import path
from .views import ProductListCreateView, AdminProductListCreateView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list'),
    path('admin/', AdminProductListCreateView.as_view())
]