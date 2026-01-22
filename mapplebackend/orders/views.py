import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart, CartItem   # ← import Cart too
from .models import Order, OrderItem
from rest_framework.generics import RetrieveAPIView
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.generics import ListAPIView
from rest_framework import permissions, status
from django.db.models import Sum
from products.models import Product



class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        order_type = request.query_params.get("type", "cart")

        items = []
        total_amount = 0

        # -------------------------
        # CART CHECKOUT (existing)
        # -------------------------
        if order_type == "cart":
            try:
                cart = Cart.objects.get(user=user)
            except Cart.DoesNotExist:
                return Response({"detail": "Cart not found"}, status=400)

            cart_items = CartItem.objects.filter(cart=cart)
            if not cart_items.exists():
                return Response({"detail": "Cart is empty"}, status=400)

            for item in cart_items:
                total_amount += item.product.price * item.quantity
                items.append({
                    "product": item.product,
                    "quantity": item.quantity,
                    "price": item.product.price
                })

        # -------------------------
        # SINGLE PRODUCT CHECKOUT
        # -------------------------
        elif order_type == "single":
            product_id = request.query_params.get("product_id")
            if not product_id:
                return Response({"detail": "Product ID required"}, status=400)

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({"detail": "Product not found"}, status=404)

            total_amount = product.price
            items.append({
                "product": product,
                "quantity": 1,
                "price": product.price
            })

        else:
            return Response({"detail": "Invalid order type"}, status=400)

        # Razorpay uses paise
        total_paise = int(total_amount * 100)

        # Create Razorpay order
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        razorpay_order = client.order.create({
            "amount": total_paise,
            "currency": "INR",
            "payment_capture": 1
        })

        # Create Order in DB
        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            razorpay_order_id=razorpay_order["id"],
            status="PENDING",
            order_type=order_type
        )

        # Create OrderItems
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                price=item["price"]
            )

        return Response({
            "order_id": razorpay_order["id"],
            "amount": total_paise,
            "currency": "INR",
            "key": settings.RAZORPAY_KEY_ID,
            "order_db_id": order.id
        })



class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_payment_id = data.get("razorpay_payment_id")
        razorpay_signature = data.get("razorpay_signature")

        if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
            return Response({"detail": "Missing payment fields"}, status=400)

        try:
            # Verify signature
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
        except razorpay.errors.SignatureVerificationError:
            return Response({"detail": "Invalid signature"}, status=400)

        # Payment is valid -> update order
        try:
            order = Order.objects.get(razorpay_order_id=razorpay_order_id, user=user)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found"}, status=404)

        order.status = 'PAID'
        order.razorpay_payment_id = razorpay_payment_id
        order.razorpay_signature = razorpay_signature
        order.save()

        # Clear cart
        user_cart = Cart.objects.get(user=user)
        CartItem.objects.filter(cart=user_cart).delete()

        return Response({"success": True, "message": "Payment verified"})
    
class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response(
                {"detail": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderSerializer(order)
        return Response(serializer.data)

    
class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
class AdminStatsViews(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        total_products = OrderItem.objects.aggregate(
            total = Sum('quantity')
        )['total'] or 0
    
        total_revenue = Order.objects.filter(status='PAID').aggregate(
            revenue = Sum('total_amount')
        )['revenue'] or 0

        total_orders = Order.objects.count()

        paid_orders = Order.objects.filter(status='PAID').count()

        return Response(
            {
                "total_products_purchased": total_products,
                "total_revenue": total_revenue,
                "total_orders": total_orders,
                "paid_orders": paid_orders,
            }
        )
    
class AdminOrderListView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        orders = Order.objects.all().order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AdminOrderDetailView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {"detail": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


    
class AdminOrderStatusUpdateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {"detail": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        status_value = request.data.get("status")
        if not status_value:
            return Response(
                {"detail": "Status is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = status_value
        order.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    