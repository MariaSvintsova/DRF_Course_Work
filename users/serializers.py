from rest_framework import serializers

from users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    """
    Serializer for user registration.

    Includes fields:
    - username (str): Username of the user.
    - email (str): Email address of the user.
    - phone (str): Phone number of the user.
    - password (str): Write-only field for setting user password.

    """

    class Meta:
        model = User
        fields = "__all__"

    def save(self, validated_data):
        """Create and save a new user instance with validated data."""
        password = self.validated_data['password']

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            password=validated_data['password']
        )
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user details.

    Includes fields:
    - username (str): Username of the user.
    - email (str): Email address of the user.
    - phone (str): Phone number of the user.

    """

    class Meta:
        model = User
        fields = "__all__"