from rest_framework.views import APIView
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(
            user=request.user,
        ).order_by("-created_at")

        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MarkNotificationReadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, notification_id):
        notification = Notification.objects.filter(
            id=notification_id,
            user=request.user
        ).first()

        if not notification:
            return Response(
                {"detail": "Not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        notification.is_read = True
        notification.save()

        return Response(
            {"success": True},
            status=status.HTTP_200_OK
        )
    
class CreateNotificationView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        notification = serializer.save(user=request.data["user"])

        return Response(
            NotificationSerializer(notification).data,
            status=status.HTTP_201_CREATED
        )


    
