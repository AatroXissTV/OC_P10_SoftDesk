# django imports
from django.contrib.auth import get_user_model

# django rest framework imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle

# django rest framework simplejwt imports
from rest_framework_simplejwt.views import TokenViewBase


# local imports
from .serializers import UserSerializer, MyTokenObtainSerializer

User = get_user_model()


class CreateUserView(APIView):

    throttle_classes = [UserRateThrottle]
    serializer_class = UserSerializer

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MyTokenObtainView(TokenViewBase):
    serializer_class = MyTokenObtainSerializer
