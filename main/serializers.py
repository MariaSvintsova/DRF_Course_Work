from rest_framework import serializers
from main.models import Habit

class HabitSerializer(serializers.ModelSerializer):
    """ Serializer for habits """
    class Meta:
        model = Habit
        fields = '__all__'
