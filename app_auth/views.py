from django.contrib.auth import get_user_model
from .serializers import SignUpSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny

User = get_user_model()


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    permissions_classes = (AllowAny,)
    serializer_class = SignUpSerializer
