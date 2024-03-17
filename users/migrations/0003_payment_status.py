# Generated by Django 5.0.2 on 2024-03-16 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('closed', 'Closed'), ('canceled', 'Canceled')], default='OPEN', max_length=8, verbose_name='статус оплаты'),
        ),
    ]