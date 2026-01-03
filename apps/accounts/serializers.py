from rest_framework import serializers
from .models import User

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "phone", "name", "email")

# accounts/serializers.py
from rest_framework import serializers
from .models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "phone",
            "name",
            "email",
            "created_at",
            "last_login",
            "total_orders",
            "lifetime_value",
            "preferred_categories",
            "verification_status",
            "cod_limit",
        )
        # read_only_fields = fields
        read_only_fields = (
            "id",
            "phone",
            "created_at",
            "last_login",
            "total_orders",
            "lifetime_value",
            "verification_status",
            "cod_limit",
        )
