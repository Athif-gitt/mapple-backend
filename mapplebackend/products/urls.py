from django.urls import path
from .views import ProductListCreateView, AdminProductListCreateView, AdminProductDetailView, ProductDetailView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('admin/', AdminProductListCreateView.as_view()),
    path('admin/<int:pk>/', AdminProductDetailView.as_view())
]