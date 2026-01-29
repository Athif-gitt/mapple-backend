from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from products.models import Product
from reviews.models import Review
from reviews.serializers import ReviewSerializer

from django.shortcuts import get_object_or_404

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class ProductReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        serializer = ReviewSerializer(
            data=request.data,
            context={
                "request": request,
                "product": product,
            }
        )

        if serializer.is_valid():
            review = serializer.save(user=request.user, product=product)

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"reviews_{product.id}",
                {
                    "type": "review_created",
                    "data": {
                        "id": review.id,
                        "user": request.user.username,
                        "rating": review.rating,
                        "comment": review.comment,
                        "created_at": review.created_at.isoformat(),
                    },
                },
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductReviewListView(APIView):
    def get(self, request, product_id):
        reviews = Review.objects.filter(product_id=product_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
