# Generated by Django 4.0.2 on 2022-04-07 01:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0012_task_users_submitted'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='room_members', to=settings.AUTH_USER_MODEL),
        ),
    ]
