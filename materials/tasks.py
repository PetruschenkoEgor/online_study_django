from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


@shared_task
def send_mail_after_update_course(email):
    """Отправка письма об обновлении курса"""

    print("еще не отправилось")
    send_mail(
        "Обновление курса",
        "Вышло обновление курса! Скорее проверь, что изменилось!",
        EMAIL_HOST_USER,
        email,
    )
    print("Отправилось")
