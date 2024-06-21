from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

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
        # Проверяем, что поле is_pleasant_habit существует в модели Habit
        if hasattr(Habit, 'is_pleasant_habit'):
            return Habit.objects.filter(user=user, is_pleasant_habit=True, is_published=True)
        else:
            return Habit.objects.filter(user=user, is_published=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ View for habit's details  """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(self.queryset, pk=pk)


class HabitCreateView(generics.CreateAPIView):
    """ View for creating habit  """
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.data  # Получаем данные напрямую из аргументов функции
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HabitUpdateAPIView(generics.UpdateAPIView):
    """ View for upating habit  """
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwnerOrReadOnly]


class HabitDestroyAPIView(generics.DestroyAPIView):
    """ View for deleting habit  """
    queryset = Habit.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
