from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')
    phone = models.CharField(max_length=50, verbose_name='Телефон', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='Город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/image', verbose_name='Аватар', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ('id',)


class Payment(models.Model):
    class PaymentType(models.TextChoices):
        CASH = 'cash', 'Наличными'
        BANK = 'bank', 'Перевод на счёт'

    payer = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='плательщик', related_name='payer')
    date_of_payment = models.DateField(auto_now=True, verbose_name='дата оплаты')
    payed_course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name='оплаченный курс')
    payed_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, **NULLABLE, verbose_name='оплаченный урок')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='сумма оплаты')
    payment_type = models.CharField(max_length=20, choices=PaymentType.choices, verbose_name='способ оплаты')

    def __str__(self):
        return f'{self.payer} - {self.payed_course if self.payed_course else self.payed_lesson} - {self.amount}'

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = 'оплаты'
        ordering = ('payer', 'date_of_payment')

