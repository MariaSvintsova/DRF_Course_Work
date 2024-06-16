from rest_framework import serializers

from users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def save(self, validated_data):
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

    class Meta:
        model = User
        fields = "__all__"