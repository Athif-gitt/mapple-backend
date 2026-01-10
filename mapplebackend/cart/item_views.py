from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import CartItem

class CartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):
        action = request.data.get("action")
        try:
            item = CartItem.objects.get(id=item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({
                "error": "Item not found",
            }, status=status.HTTP_404_NOT_FOUND)

        if action == 'inc':
            item.quantity += 1
            item.save()
        
        elif action == "dec":
            item.quantity -= 1
            if item.quantity <= 0:
                item.delete()
                return Response({"message": "Item removed"})
            item.save()
        else:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Quantity updated"})
    
    def delete(self, request, item_id):
        try:
            item = CartItem.objects.get(id=item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response({"message": "Item removed"}, status=status.HTTP_204_NO_CONTENT)

