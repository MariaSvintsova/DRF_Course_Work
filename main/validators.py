from datetime import timedelta
from rest_framework.exceptions import ValidationError


class RewardAndRelatedHabitsValidator:
    """ Validator for checking related habits """
    def __call__(self, instance):
        if instance.related_habit and instance.reward:
            raise ValidationError("В модели не должно быть заполнено одновременно и поле вознаграждения, и поле связанной привычки. Можно заполнить только одно из двух полей")


class DurationValidator:
    """ Validator for checking duration """
    def __call__(self, instance):
        if instance.duration > timedelta(seconds=120):
            raise ValidationError("Время выполнения должно быть не больше 120 секунд.")


class RelatedHabitsValidator:
    """ Validator for checking related habits """
    def __call__(self, instance):
        if instance.related_habit and not instance.is_pleasant:
            raise ValidationError("В связанные привычки могут попадать только привычки с признаком приятной привычки.")


class PleasantHabitsValidator:
    """ Validator for checking if pleasant habit has reward or related habit """
    def __call__(self, instance):
        if instance.is_pleasant and instance.related_habit != None or instance.is_pleasant and instance.reward != None:
            raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")
