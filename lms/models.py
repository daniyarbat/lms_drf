from django.db import models
from django.utils import timezone

from config import settings

NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    preview = models.ImageField(upload_to='course_images/', **NULLABLE, verbose_name='Превью')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              verbose_name='автор курса', **NULLABLE)
    price = models.PositiveIntegerField(default=1000, verbose_name='Цена курса')
    updated_at = models.DateTimeField(default=timezone.now, verbose_name='последнее обновление')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ('title',)


class Lesson(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    preview = models.ImageField(upload_to='lesson_images/', **NULLABLE, verbose_name='Превью')
    link = models.URLField(**NULLABLE, verbose_name='ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', related_name='lessons')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              verbose_name='автор урока', **NULLABLE)
    price = models.PositiveIntegerField(default=100, verbose_name='Цена урока')
    updated_at = models.DateTimeField(default=timezone.now, verbose_name='последнее обновление')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = ('title',)


class CourseSubscription(models.Model):
    is_subscribed = models.BooleanField(default=False, verbose_name='подписка', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', related_name='subscription')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='пользователь', on_delete=models.CASCADE,
                             related_name='course_user', **NULLABLE)

    def __str__(self):
        return f'Курс {self.course} - подписка {self.is_subscribed}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
