# Generated by Django 5.0.2 on 2024-03-10 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0003_coursesubscription'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coursesubscription',
            old_name='user',
            new_name='owner',
        ),
    ]