from django.urls import path

from main.views import HabitDestroyAPIView, HabitUpdateAPIView, HabitCreateView, HabitViewSet, HabitDetailView

urlpatterns = [
    path('habits/', HabitViewSet.as_view({'get': 'list'}), name='habit-list'),
    path('<int:pk>/', HabitDetailView.as_view(), name='habit-detail'),
    path('create/', HabitCreateView.as_view(), name='habit-create'),
    path('/update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit-update'),
    path('/delete/<int:pk>/', HabitDestroyAPIView.as_view(), name='habit-delete'),
]