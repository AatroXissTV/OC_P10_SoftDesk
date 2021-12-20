# django imports
from django.contrib.auth import get_user_model
# from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

# django rest framework imports
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    PasswordField,
    TokenObtainSerializer
)
from rest_framework_simplejwt.tokens import AccessToken

# Get custom user model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = PasswordField(write_only=True)
    password_confirmation = PasswordField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password',
            'email',
            'password_confirmation']

    def get_validation(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError(
                'Password and password confirmation must match.'
            )
        validate_password(data['password'])
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class MyTokenObtainSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return AccessToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        access = self.get_token(self.user)
        data['access'] = str(access)
