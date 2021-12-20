# django imports
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

# django rest framework imports
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken

# Get custom user model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    # passwords & password_confirmation
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )

    password_confirmation = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'password_confirmation'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirmation': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError(
                {'Password': 'Passwords do not match'})
        elif len(data['password']) < 8:
            raise serializers.ValidationError(
                {'Password': 'Password must be at least 8 characters long'})
        return data


class MyTokenObtainSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return AccessToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['access'] = str(refresh)
