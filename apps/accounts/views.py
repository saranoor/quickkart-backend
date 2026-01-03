from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ValidationError

from .serializers import UserProfileUpdateSerializer, UserProfileSerializer

User = get_user_model()

class UserProfileView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        print("Request user:", request.user)
        email = request.query_params.get("email")
        print("Email param:", email)

        if email:
            # INTERNAL USE: lookup by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise NotFound("User with this email does not exist")
        else:
            user = request.user

        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request):
            # TO DO:
            test_user = User.objects.get(phone="1234567890")
            # request.user is now guaranteed to be a real User object
            serializer = UserProfileSerializer(test_user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
    
    # # def put(self, request):

    #     if request.user.is_anonymous:
    #         user = User.objects.first()  # TEMP ONLY
    #     else:
    #         user = request.user
    #     email = request.query_params.get("email")

    #     if email:
    #         # internal update
    #         if not request.user.is_staff:
    #             raise ValidationError("Not allowed")
    #         try:
    #             user = User.objects.get(email=email)
    #         except User.DoesNotExist:
    #             raise NotFound("User not found")
    #     else:
    #         user = request.user

    #     serializer = UserProfileUpdateSerializer(
    #         user,
    #         data=request.data,
    #         partial=True
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return Response(
    #         UserProfileSerializer(user).data,
    #         status=status.HTTP_200_OK
    #     )