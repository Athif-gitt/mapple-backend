from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Address
        read_only_fields = ("user",)
        