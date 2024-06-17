from asgiref.sync import sync_to_async
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import User
from users.serializers import UserSerializer, RegisterSerializer

class UserListAPIView(generics.ListAPIView):
    """List all users."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class RegisterAPIView(generics.CreateAPIView):
    """Register a new user."""
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    @staticmethod
    @sync_to_async
    def create_user(username, phone, bot_id, password):
        """Create a new user."""
        User.objects.create(username=username, phone=phone, bot_id=bot_id, password=password)


class UserDetailView(generics.RetrieveAPIView):
    """Retrieve user details."""
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateView(generics.UpdateAPIView):
    """Update user details."""
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(generics.DestroyAPIView):
    """Delete a user."""
    serializer_class = UserSerializer
    queryset = User.objects.all()


