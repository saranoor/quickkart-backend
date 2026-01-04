from django.urls import path
from .views import UserProfileView, RequestOTPView, VerifyOTPView

urlpatterns = [
    path("auth/request-otp/", RequestOTPView.as_view()),
    path("auth/verify-otp/", VerifyOTPView.as_view()),
    path("user/profile", UserProfileView.as_view(), name="user-profile"),
]
