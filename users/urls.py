from django.urls import path
from users.views import UserListAPIView, RegisterAPIView, UserDestroyAPIView, UserUpdateView, UserDetailView

app_name = 'users'

urlpatterns = [
    path('', UserListAPIView.as_view(), name='user-list'),
    path('register/', RegisterAPIView.as_view(), name='user-register'),
    path('detail/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user-destroy'),  # Изменил с 'detail' на 'delete'
]
