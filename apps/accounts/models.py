from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    name = models.CharField(max_length=255)

    # business metrics
    total_orders = models.PositiveIntegerField(default=0)
    lifetime_value = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    cod_limit = models.PositiveIntegerField(default=500)

    # preferences & status
    preferred_categories = models.JSONField(default=list, blank=True)
    verification_status = models.CharField(
        max_length=20,
        choices=[
            ("unverified", "Unverified"),
            ("verified", "Verified"),
            ("blocked", "Blocked"),
        ],
        default="unverified",
    )

    # system fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return f"{self.phone} - {self.name}"
