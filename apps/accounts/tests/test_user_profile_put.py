from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from apps.accounts.models import User
from django.urls import reverse

class UserProfilePutTests(APITestCase):
    url = reverse("user-profile")

    def authenticate(self, user):
        token = AccessToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )

    def test_put_profile_updates_allowed_fields(self):
        user = User.objects.create(
            phone="+923001234567",
            name="Old Name",
            email="old@example.com",
            is_active=True,
        )

        self.authenticate(user)

        payload = {
            "name": "New Name",
            "email": "new@example.com",
            "preferred_categories": ["dairy", "bakery"],
        }

        response = self.client.put(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user.refresh_from_db()
        self.assertEqual(user.name, "New Name")
        self.assertEqual(user.email, "new@example.com")
        self.assertEqual(user.preferred_categories, ["dairy", "bakery"])

    def test_put_profile_unauthenticated_fails(self):
        response = self.client.put(
            self.url,
            {"name": "Hacker"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
