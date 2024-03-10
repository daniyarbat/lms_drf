# Generated by Django 5.0.2 on 2024-03-10 07:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0002_course_owner_lesson_owner_alter_lesson_course'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_subscribed', models.BooleanField(blank=True, default=False, null=True, verbose_name='подписка')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to='lms.course', verbose_name='курс')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_user', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'подписка',
                'verbose_name_plural': 'подписки',
            },
        ),
    ]
