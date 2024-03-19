# from django.utils.datetime_safe import datetime
# from django_celery_beat.models import CrontabSchedule
from django.http import HttpResponse
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from datetime import datetime
from django.utils import timezone
import pytz
from habit.models import Habit
from habit.tasks import send_telegram_message


def check_habits_daily():
    """ Проверка ежедневных привычек на выполнение """

    date_time_now = datetime.now()
    moscow_timezone = pytz.timezone('Europe/Moscow')
    date_now = date_time_now.astimezone(moscow_timezone)
    time_now = date_now.time()

    habits = Habit.objects.filter(time__hour=time_now.hour, time__minute=time_now.minute,
                                  periodicity='Каждый день', nice=False)

    for habit in habits:
        create_message(habit.id)


def check_habits_weekly():
    """ Проверка еженедельных привычек на выполнение """

    date_time_now = datetime.now()
    moscow_timezone = pytz.timezone('Europe/Moscow')
    date_now = date_time_now.astimezone(moscow_timezone)
    time_now = date_now.time()

    habits = Habit.objects.filter(time__hour=time_now.hour, time__minute=time_now.minute,
                                  periodicity='Каждая неделя', nice=False)

    for habit in habits:
        create_message(habit.id)


def create_message(habit_id):
    """ Функция создания сообщения для отправки в телеграм-бот """

    habit = Habit.objects.get(id=habit_id)

    user = habit.user
    time = habit.time
    action = habit.action
    place = habit.place
    duration = habit.duration.total_seconds()

    message = f'''Привет {user}! {time} в {place} необходимо выполнять {action} в течение {duration} !'''

    response = send_telegram_message(habit.telegram, message)
    if habit.related_habit:
        message = f'''{habit.user}, молодец! Ты выполнил {habit.action} и получаешь награду: {habit.reward}'''
        time.sleep(10)
        nice_response = send_telegram_message(habit.telegram, message)
        return HttpResponse(nice_response)

    return HttpResponse(response)


def create_habit_schedule(habit):
    """Создание периодичности и задачи на отправку"""
    crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
        minute=habit.time.minute,
        hour=habit.time.hour,
        day_of_month='*',
        month_of_year='*',
        day_of_week='*',
        timezone='Europe/Moscow'
    )

    PeriodicTask.objects.create(
        crontab=crontab_schedule,
        name=f'Habit Task - {habit.place}',
        task='tracker.tasks.send_telegram_message',
        args=[habit.id],
    )

    def delete_reminder(habit):
        """ Удаление задачи """

        task_name = f'send_message_to_bot_{habit.id}'
        PeriodicTask.objects.filter(name=task_name).delete()

    def update_reminder(habit):
        """ Обновление задачи """

        delete_reminder(habit)
        create_habit_schedule(habit)
