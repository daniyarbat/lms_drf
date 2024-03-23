# Generated by Django 5.0.2 on 2024-03-23 08:07

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0006_lesson_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='последнее обновление'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='последнее обновление'),
        ),
    ]
