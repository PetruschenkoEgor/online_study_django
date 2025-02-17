import datetime

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def check_user():
    """Проверка пользователя по дате последнего входа и блокировка пользователя, если он не заходил больше месяца."""
    now = timezone.now()
    users = User.objects.all()
    for user in users:
        if (
            user.last_login is not None
            and (user.last_login + datetime.timedelta(days=30)) < now
        ):
            user.is_active = False
            user.save()
            print("Пользователь заблокирован")
        else:
            print("Пользователь активен")
