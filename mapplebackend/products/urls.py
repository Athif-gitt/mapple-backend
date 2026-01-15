from django.urls import path
from .views import ProductListCreateView, AdminProductListCreateView, AdminProductDetailView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list'),
    path('admin/', AdminProductListCreateView.as_view()),
    path('admin/<int:pk>/', AdminProductDetailView.as_view())
]