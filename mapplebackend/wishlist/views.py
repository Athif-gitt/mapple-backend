from rest_framework.response import Response
from rest_framework.views  import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from products.models import Product
from .models import Wishlist, WishlistItem
from .serializers import WishlistItemSerializer
from rest_framework import status

class WishlistView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        items = wishlist.item.all()
        return Response(WishlistItemSerializer(items, many=True).data)

    def post(self, request):
        product_id = request.data.get('product_id')
        product = Product.objects.get(id=product_id)
        wishlist = request.user.wishlist

        item, created = WishlistItem.objects.get_or_create(
            wishlist = wishlist,
            product = product
        )
        return Response(WishlistItemSerializer(item).data, status )
    
class WishlistItemDeleteView(APIView):
        permission_classes = [IsAuthenticated]

        def delete(self, request, pk):
            wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
            WishlistItem.objects.get(pk=pk, wishlist=request.user.wishlist).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    

