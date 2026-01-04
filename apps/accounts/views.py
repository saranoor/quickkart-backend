from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserProfileSerializer
from .models import User
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import random

from .models import OTP, User

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class RequestOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone")

        if not phone:
            return Response({"error": "phone required"}, status=400)

        otp = str(random.randint(100000, 999999))
        OTP.objects.create(phone=phone, code=otp)

        print("DEV OTP:", otp)  # SMS in prod

        return Response({"message": "OTP sent"})
    
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone")
        code = request.data.get("otp")

        otp = OTP.objects.filter(phone=phone, code=code).last()

        if not otp or otp.is_expired():
            return Response({"error": "Invalid OTP"}, status=400)

        user, _ = User.objects.get_or_create(
            phone=phone,
            defaults={"name": "New User"}
        )

        user.verification_status = "verified"
        user.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
        })
