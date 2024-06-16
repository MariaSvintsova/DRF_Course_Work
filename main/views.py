from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from main.models import Habit
from main.paginators import HabitsPagination
from main.permissions import IsOwnerOrReadOnly
from main.serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    """ ViewSet for habits """

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitsPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Habit.objects.all()
        else:
            return Habit.objects.filter(user=user, is_pleasant_habit=True, is_published=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(self.queryset, pk=pk)


class HabitCreateView(generics.CreateAPIView):
    serializer_class = HabitSerializer

    def post(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()


class HabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwnerOrReadOnly]


class HabitDestroyAPIView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    permission_classes = [IsOwnerOrReadOnly]




