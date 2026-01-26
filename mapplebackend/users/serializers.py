from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authentication import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User already exist")
        return value
    
    def validate_password(self, value):
        validate_password(value)
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user
    

    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            username=data["username"],
            password=data["password"]
        )

        if not user:
            raise serializers.ValidationError("Invalid Credentiels")
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_staff', 'is_active']


class ProfileSummarySerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    is_verified = serializers.SerializerMethodField()
    joined_at = serializers.DateTimeField(source="user.date_joined", read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            "full_name",
            "email",
            "phone",
            "avatar",
            "is_verified",
            "joined_at",
        )

    def get_is_verified(self, obj):
        return True


