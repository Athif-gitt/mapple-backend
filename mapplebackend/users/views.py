from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.conf import settings
from django.shortcuts import redirect
from django.utils.timezone import now
from datetime import timedelta

from oauth2_provider.models import Application, AccessToken, RefreshToken
from oauthlib.common import generate_token


class RegisterApiView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "User created",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class LoginApiView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login successful",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    
class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response ({
            "username": request.user.username,
            "is_staff": request.user.is_staff,
        })
    
class AdminUserListView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
    
class AdminUserDetailsList(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User does not exist"}, status=status.HTTP_404_NOT_FOUND) 
        
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class AdminUserBlockView(APIView):
    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if user == request.user:
            return Response(
                {"detail": "You cannot block yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.is_active = not user.is_active
        user.save()
        return Response({
            "id": user.id,
            "is_active": user.is_active,
            "message": "User unblocked" if user.is_active else "User blocked"
        }, status=status.HTTP_200_OK) 
    
def google_login_success(request):
    user = request.user

    if not user.is_authenticated:
        return redirect(f"{settings.FRONTEND_URL}/login?error=google")

    app = Application.objects.get(name="mapple-frontend")

    access_token = AccessToken.objects.create(
        user=user,
        application=app,
        token=generate_token(),
        expires=now() + timedelta(hours=10),
        scope="read write",
    )

    refresh_token = RefreshToken.objects.create(
        user=user,
        application=app,
        token=generate_token(),
        access_token=access_token,
    )

    return redirect(
        f"{settings.FRONTEND_URL}/oauth/callback"
        f"?access={access_token.token}"
        f"&refresh={refresh_token.token}"
    )
        

            
    
