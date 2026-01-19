from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)

    total_orders = models.PositiveIntegerField(default=0)
    lifetime_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    preferred_categories = models.JSONField(default=list, blank=True)

    verification_status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("verified", "Verified"),
            ("blocked", "Blocked"),
        ],
        default="pending"
    )

    cod_limit = models.PositiveIntegerField(default=500)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return f"{self.phone} - {self.name}"


class OTP(models.Model):
    phone = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        print(f"is the token expired: {timezone.now() > self.created_at + timedelta(minutes=50)}")
        return timezone.now() > self.created_at + timedelta(minutes=50)