from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Notification


def notify_user(user, title, message):
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message,
    )

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}_notifications",
        {
            "type": "send_notification",
            "data": {
                "id": notification.id,
                "title": notification.title,
                "message": notification.message,
                "is_read": notification.is_read,
                "created_at": notification.created_at.isoformat(),
            },
        },
    )

    return notification
