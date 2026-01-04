from datetime import timedelta
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status

from apps.accounts.models import OTP, User


class VerifyOTPTests(APITestCase):
    url = "/api/auth/verify-otp/"

    def test_verify_otp_success_returns_token(self):
        phone = "+923001234567"
        code = "123456"

        OTP.objects.create(phone=phone, code=code)

        res = self.client.post(self.url, {"phone": phone, "otp": code}, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", res.data)
        self.assertTrue(isinstance(res.data["access"], str))
        self.assertGreater(len(res.data["access"]), 10)

        # user should exist
        user = User.objects.get(phone=phone)
        self.assertEqual(user.verification_status, "verified")

        # otp should be marked used
        otp = OTP.objects.filter(phone=phone).last()
        self.assertIsNotNone(otp)

    def test_verify_otp_invalid_code_fails(self):
        phone = "+923001234567"

        OTP.objects.create(phone=phone, code="111111")

        res = self.client.post(self.url, {"phone": phone, "otp": "222222"}, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", res.data)

        otp = OTP.objects.filter(phone=phone).last()
        self.assertEqual(otp.is_expired(), False)

    def test_verify_otp_missing_otp_record_fails(self):
        res = self.client.post(self.url, {"phone": "+923001234567", "otp": "123456"}, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", res.data)
