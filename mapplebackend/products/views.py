from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')

        if category:
            queryset = queryset.filter(category__iexact=category)

        if search:
            queryset = queryset.filter(
                name__icontains=search
            ) | queryset.filter(
                description__icontains=search
            )

        return queryset

