from django.core.management import BaseCommand
import datetime

from lms.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    help = 'Create sample payment objects'

    def handle(self, *args, **kwargs):
        # Очистить содержимое моделей перед созданием новых объектов
        Payment.objects.all().delete()
        # User.objects.all().delete()

        # Создаем пользователей, курсы и уроки (если они еще не созданы)
        user1, created = User.objects.get_or_create(email='test1@sky.pro')
        user2, created = User.objects.get_or_create(email='test2@sky.pro')

        # Создаём платежи
        payment1 = Payment.objects.create(
            payer=user1,
            date_of_payment=datetime.datetime.now().date(),
            amount=10000,
            payment_type='cash',
            payed_course=Course.objects.get(pk=2),
        )

        payment2 = Payment.objects.create(
            payer=user2,
            date_of_payment=datetime.datetime.now().date(),
            amount=100000,
            payment_type='bank',
            payed_lesson=Lesson.objects.get(pk=1),
        )

        payment3 = Payment.objects.create(
            date_of_payment=datetime.datetime.now().date(),
            amount=50000,
            payment_type='bank',
            payed_lesson=Lesson.objects.get(pk=2),
        )

        self.stdout.write(self.style.SUCCESS('Объекты оплаты успешно загружены'))
