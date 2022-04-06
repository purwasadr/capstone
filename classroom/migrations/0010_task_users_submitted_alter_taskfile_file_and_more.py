# Generated by Django 4.0.2 on 2022-04-06 14:45

import classroom.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0009_task_due_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='users_submitted',
            field=models.ManyToManyField(blank=True, related_name='submitted_tasks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='taskfile',
            name='file',
            field=models.FileField(upload_to=classroom.models.task_directory_path),
        ),
        migrations.CreateModel(
            name='TaskSubmitFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(default='', max_length=3000)),
                ('file', models.FileField(upload_to=classroom.models.task_submit_directory_path)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submitted_files', to='classroom.task')),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submitted_task_files', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TaskSubmit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
