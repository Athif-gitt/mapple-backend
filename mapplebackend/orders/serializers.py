from rest_framework import serializers
from .models import Order, OrderItem, OrderAddress
from products.serializers import ProductSerializer  

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAddress
        fields = [
            "full_name",
            "phone",
            "line1",
            "line2",
            "city",
            "state",
            "pincode",
            "country",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    delivery_address = OrderAddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_type",
            "total_amount",
            "status",
            "created_at",
            "items",
            "delivery_address",
        ]

class RecentOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "id",
            "total_amount",
            "status",
            "created_at",
        )



