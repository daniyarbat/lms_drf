# Generated by Django 5.0.2 on 2024-03-17 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0005_course_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='price',
            field=models.PositiveIntegerField(default=100, verbose_name='Цена урока'),
        ),
    ]
