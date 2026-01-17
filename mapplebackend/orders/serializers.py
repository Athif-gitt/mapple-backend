from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer  

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'total_amount', 'status',
            'razorpay_order_id', 'created_at', 'items', 'username'
        ]
        read_only_fields = ['user', 'status', 'razorpay_order_id']
