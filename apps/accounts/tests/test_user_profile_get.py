from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import User
from rest_framework_simplejwt.tokens import AccessToken
from django.urls import reverse

class UserProfileGetTests(APITestCase):
    url = reverse("user-profile")

    def authenticate(self, user):
        token = AccessToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )

    def test_get_profile_success(self):
        user = User.objects.create(
            phone="+923001234567",
            name="Sara Noor",
            email="sara@example.com",
            verification_status="verified",
            total_orders=5,
            lifetime_value=2500,
            is_active=True,
        )
        self.authenticate(user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_profile_unauthenticated_fails(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_response_fields(self):
        user = User.objects.create(
            phone="+923001234567",
            name="Sara Noor"
        )

        self.authenticate(user)
        response = self.client.get(self.url)

        expected_fields = {
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
        }

        self.assertEqual(set(response.data.keys()), expected_fields)

    def test_get_profile_returns_correct_user(self):
        user1 = User.objects.create(phone="+923001111111", name="User One")
        user2 = User.objects.create(phone="+923002222222", name="User Two")

        self.authenticate(user1)
        response = self.client.get(self.url)

        self.assertEqual(response.data["phone"], user1.phone)
        self.assertNotEqual(response.data["phone"], user2.phone)

    def test_internal_fields_not_exposed(self):
        user = User.objects.create(phone="+923001234567", name="Sara")

        self.authenticate(user)
        response = self.client.get(self.url)

        self.assertNotIn("is_staff", response.data)
        self.assertNotIn("is_superuser", response.data)
        self.assertNotIn("password", response.data)
