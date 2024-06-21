import os

import pytest

from users.serializers import RegisterSerializer
# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
# Ensure settings are configured before importing django modules

import django
django.setup()

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from main.models import Habit
from main.serializers import HabitSerializer
from datetime import time, timedelta
import json

User = get_user_model()
@pytest.mark.django_db
def test_create_habit():
    client = APIClient()
    user = User.objects.create(username='testuser', password='testpassword')
    client.force_authenticate(user=user)

    habit_data = {
        'title': 'Test Habit',
        'bot_id': 123456789,
        'place': 'Test Place',
        'time': '08:00:00',
        'action': 'Test Action',
        'is_useful': True,
        'is_pleasant': True,
        'frequency': 'daily',
        'duration': timedelta(minutes=1),
        'is_published': True,
        'related_habit': None,
        'reward': None
    }

    response = client.post(reverse('main:habit-create'), habit_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_update_habit_url():
    client = APIClient()
    user = User.objects.create(username='testuser', password='testpassword')
    client.force_authenticate(user=user)

    habit = Habit.objects.create(user=user, title='Old Title', place='Old Place', time='08:00:00',
                                 action='Old Action', is_useful=True, is_pleasant=True,
                                 frequency='daily', duration='00:10:00', is_published=True)

    updated_data = {
        'title': 'Updated Title',
        'place': 'Updated Place',
    }

    response = client.patch(reverse('main:habit-update', kwargs={'pk': habit.pk}), updated_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == 'Updated Title'

@pytest.mark.django_db
def test_delete_habit_url():
    client = APIClient()
    user = User.objects.create(username='testuser', password='testpassword')
    client.force_authenticate(user=user)

    habit = Habit.objects.create(user=user, title='Test Habit', place='Test Place', time='08:00:00',
                                 action='Test Action', is_useful=True, is_pleasant=True,
                                 frequency='daily', duration='00:10:00', is_published=True)

    response = client.delete(reverse('main:habit-delete', kwargs={'pk': habit.pk}))
    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db
def test_list_habits_url():
    client = APIClient()
    user = User.objects.create(username='testuser', password='testpassword')
    client.force_authenticate(user=user)

    Habit.objects.create(user=user, title='Habit 1', place='Place 1', time='08:00:00',
                         action='Action 1', is_useful=True, is_pleasant=True,
                         frequency='daily', duration='00:10:00', is_published=True)
    Habit.objects.create(user=user, title='Habit 2', place='Place 2', time='09:00:00',
                         action='Action 2', is_useful=True, is_pleasant=False,
                         frequency='weekly', duration='00:15:00', is_published=True)

    response = client.get(reverse('main:habit-list'))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2  ## Assuming there are exactly 2 habits for this user

@pytest.mark.django_db
def test_register_user_url():
    client = APIClient()

    user_data = {
        'username': 'newuser',
        'password': 'newpassword',
    }


    serializer = RegisterSerializer(data=user_data)
    assert serializer.is_valid()

    response = client.post(reverse('users:user-register'), serializer.validated_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    created_user = User.objects.get(username=user_data['username'])
    assert created_user is not None

@pytest.mark.django_db
def test_delete_user_url():
    client = APIClient()
    user = User.objects.create(username='testuser', password='testpassword')
    client.force_authenticate(user=user)

    response = client.delete(reverse('users:user-destroy', kwargs={'pk': user.pk}))
    assert response.status_code == status.HTTP_204_NO_CONTENT