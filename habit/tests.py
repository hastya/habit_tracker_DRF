from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from habit.models import Habit
from users.models import User


# Create your tests here.

class HabitListTestCase(APITestCase):
    """ТестКейсы для тестирования отображения существующих привычек"""
    maxDiff = None

    def setUp(self) -> None:
        """Предварительное наполнение БД для дальнейших тестов."""

        self.user = User.objects.create(
            email='user@email.dot',
            telegram='test_tg_username'
        )

        self.private_habit = Habit.objects.create(
            user=self.user,
            place="Тестовое место",
            time="12:00",
            action="Тестовое действие",
            duration="120",
            reward="Тестовая награда"
        )

        self.public_habit = Habit.objects.create(
            user=self.user,
            place="Место",
            time="12:00",
            action="Действие",
            duration="120",
            reward="Награда",
            is_public=True
        )

        """Имитация авторизации пользователя по JWT токену."""
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_habits_list(self):
        """Тестирование вывода списка существующих привычек"""

        response = self.client.get(reverse('tracker:habit_list'))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_get_public_habits_list(self):
        """Тестирование вывода списка существующих публичных привычек"""

        response = self.client.get(reverse('tracker:habit_public_list'))

        self.assertEqual(
            response.json(),
            {
                'count': 1,
                'next': None,
                'previous': None,
                'results':
                    [
                        {
                            'id': self.public_habit.id,
                            'user': 7,
                            'periodicity': 1,
                            'related_habit': None,
                            'place': 'Место',
                            'time': '12:00:00',
                            'action': 'Действие',
                            'nice': False,
                            'reward': 'Награда',
                            'duration': '00:02:00',
                            'is_public': True
                        }
                    ]
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


class HabitUpdateTestCase(APITestCase):
    """ТестКейсы для тестирования изменения существующих привычек при вызове PUT/PATCH методов"""

    def setUp(self) -> None:
        """Предварительное наполнение БД для дальнейших тестов."""

        self.user = User.objects.create(
            email='user@email.dot',
            telegram='test_tg_username'
        )

        self.habit = Habit.objects.create(
            user=self.user,
            place="Тестовое место",
            time="12:00",
            action="Тестовое действие",
            duration="120",
            is_public=True
        )

        """Имитация авторизации пользователя по JWT токену."""
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_patch_habit(self):
        """Тестирование обновления полей экземпляра класса 'Habit' при вызове PATCH запроса"""

        changed_data = {
            "place": "Новое измененное место",
            "action": "Новое измененное действие",
            "reward": "Новая тестовая награда"
        }

        response = self.client.patch(f'/habits/habit_update/{self.habit.id}/', data=changed_data)
        self.maxDiff = None

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


class HabitFailedCreateTestCase(APITestCase):
    """ТестКейсы для тестирования ситуаций, при которых возникают ошибки создания привычки"""

    def setUp(self) -> None:
        """Предварительное наполнение БД для дальнейших тестов."""

        self.user = User.objects.create(
            email='user@email.dot',
            telegram='test_tg_username'
        )

        """Имитация авторизации пользователя по JWT токену."""
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_habit_with_pleasure_flag(self):
        """Тестирование создания привычки с положительным флагом 'is_pleasure' """

        main_habit_data = {
            "place": "Тестовое место",
            "time": "12:00",
            "action": "Тестовое действие",
            "duration": "120",
            "is_pleasure": True
        }

        response = self.client.post(
            reverse('tracker:habit_create'),
            data=main_habit_data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_required_fields_habit(self):
        """Тестирование создание привычки без указания обязательных полей ('related_habit' / 'reward') """

        main_habit_data = {
            "place": "Тестовое место",
            "time": "12:00",
            "action": "Тестовое действие",
            "duration": "120",
        }

        response = self.client.post(
            reverse('tracker:habit_create'),
            data=main_habit_data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_overflow_field_habit(self):
        """Тестирование создания привычки при одновременном указании награды и связанной привычки"""

        related_habit_data = {
            "place": "Тестовое место связанной привычки",
            "time": "12:00",
            "action": "Тестовое действие связанной привычки",
            "duration": "120",
        }

        main_habit_data = {
            "place": "Тестовое место",
            "time": "12:00",
            "action": "Тестовое действие",
            "duration": "120",
            "related_habit": related_habit_data,
            "reward": "Тестовая награда"
        }

        response = self.client.post(
            reverse('tracker:habit_create'),
            data=main_habit_data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_execution_time_habit(self):
        """Тестирование создания привычки с указанием времени исполнения, превышающим 120 секунд"""

        main_habit_data = {
            "place": "Тестовое место",
            "time": "12:00",
            "action": "Тестовое действие",
            "duration": "130",
            "is_public": True,
        }

        response = self.client.post(
            reverse('tracker:habit_create'),
            data=main_habit_data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_execution_time_related_habit(self):
        """Тестирование создания привычки с указанием времени исполнения связанной привычки, превышающим 120 секунд"""

        related_habit_data = {
            "place": "Тестовое место связанной привычки",
            "time": "12:00",
            "action": "Тестовое действие связанной привычки",
            "duration": "130",
        }

        main_habit_data = {
            "place": "Тестовое место",
            "time": "12:00",
            "action": "Тестовое действие",
            "duration": "120",
            "related_habit": related_habit_data,
        }

        response = self.client.post(
            reverse('tracker:habit_create'),
            data=main_habit_data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
