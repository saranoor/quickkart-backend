from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.accounts.models import OTP

class RequestOTPTests(APITestCase):

    def test_request_otp_success(self):
        payload = {
            "phone": "+92300123456"
        }

        response = self.client.post(
            "/api/auth/request-otp/",
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

        # OTP should be created
        self.assertEqual(OTP.objects.count(), 1)
        self.assertEqual(OTP.objects.first().phone, payload["phone"])


    def test_request_otp_without_phone_fails(self):
        response = self.client.post(
            "/api/auth/request-otp/",
            {},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

        self.assertEqual(OTP.objects.count(), 0)
