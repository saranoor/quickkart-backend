from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserProfileSerializer
from .models import User
from rest_framework.permissions import AllowAny
from rest_framework import status


class UserProfileView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]


    def get(self, request):
        # user = User.objects.first()
        # serializer = UserProfileSerializer(request.user)
        # return Response(serializer.data)
        user = User.objects.first()
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
    def put(self, request):
        user = User.objects.first()
        print ("Request data:", request.data)
        serializer = UserProfileSerializer(
            user,
            data=request.data,
            partial=True  # allows partial updates
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
