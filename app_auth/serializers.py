from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

# Get custom user model
User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(
        write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password')

    def validate(self, value):
        if value['password'] != value['confirm_password']:
            raise serializers.ValidationError(
                {'Password': 'Passwords do not match'})
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
