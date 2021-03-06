# Generated by Django 4.0.2 on 2022-04-03 03:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0006_alter_task_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialfile',
            name='filename',
            field=models.CharField(default='', max_length=3000),
        ),
        migrations.AddField(
            model_name='taskfile',
            name='filename',
            field=models.CharField(default='', max_length=3000),
        ),
        migrations.AlterField(
            model_name='material',
            name='created_at',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='material',
            name='description',
            field=models.CharField(blank=True, max_length=3000),
        ),
        migrations.AlterField(
            model_name='room',
            name='description',
            field=models.CharField(blank=True, max_length=3000),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.CharField(blank=True, max_length=3000),
        ),
        migrations.CreateModel(
            name='MaterialComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=3000)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
