from django.urls import path, include
from rest_framework.routers import DefaultRouter
from main.views import HabitDestroyAPIView, HabitUpdateAPIView, HabitCreateView, HabitViewSet, HabitDetailView

# Создаем роутер и регистрируем ViewSet
router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habit')

urlpatterns = [
    path('', include(router.urls)),  # Включаем маршруты роутера
    path('habits/<int:pk>/', HabitDetailView.as_view(), name='habit-detail'),
    path('habits/create/', HabitCreateView.as_view(), name='habit-create'),
    path('habits/update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit-update'),
    path('habits/delete/<int:pk>/', HabitDestroyAPIView.as_view(), name='habit-delete'),
]
