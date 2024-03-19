from rest_framework.serializers import ValidationError
from datetime import timedelta


def habit_validator(value):

    time = timedelta(minutes=2)

    try:
        if value['nice']:
            if value['related_habit'] or value['reward']:
                raise ValidationError('У приятной привычки не может быть связанной привычки или вознаграждения')
    except KeyError:
        pass

    try:
        if value['related_habit'] and value['reward']:
            raise ValidationError('Можно выбрать или приятную привычку или вознаграждение')
    except KeyError:
        pass

    try:
        if value['duration'] > time:
            raise ValidationError('Привычку можно выполнять не более 120 секунд')
    except KeyError:
        pass

    try:
        if value['related_habit']:
            if not value['related_habit'].nice:
                raise ValidationError('В связанные привычки могут попадать только приятные привычки')
    except KeyError:
        pass
