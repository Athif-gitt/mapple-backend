from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile",
    )
    full_name = models.CharField(
        max_length=150,
        help_text="User's display name"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Phone number with country code"
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        help_text="Profile avatar image"
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True
    )
    gender = models.CharField(
        max_length=20,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.full_name} ({self.user.email})"

