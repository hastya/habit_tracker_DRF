from rest_framework import serializers
from habit.models import Habit
from habit.validators import habit_validator


class HabitSerializer(serializers.ModelSerializer):
    """ Сериализатор для привычки """

    class Meta:
        model = Habit
        fields = '__all__'

        validators = [
            habit_validator,
        ]
