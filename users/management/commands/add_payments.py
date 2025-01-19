
from django.core.management.base import BaseCommand
from django.utils import timezone

from materials.models import Course, Lesson
from users.models import User, Payments


class Command(BaseCommand):
    """ Кастомная команда для наполнения тестовыми данными таблицы Payments и связанных с ней таблиц """

    help = 'Add test payments to the database'

    def handle(self, *args, **kwargs):

        user, created = User.objects.get_or_create(email='petrov111@mail.ru', defaults={'phone': '89516666666', 'country': 'Россия'})

        course, created = Course.objects.get_or_create(title='Курс по Django', defaults={'description': 'Изучаем Django'})

        payment, created = Payments.objects.get_or_create(user=user, payment_date=timezone.now(), paid_course=course, defaults={'payment_amount': 10000, 'payment_method': 'Перевод на счет'})

        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully created payment for user {user.email}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Payment for user {user.email} already exists'))
