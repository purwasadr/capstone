# Generated by Django 4.0.2 on 2022-04-04 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0008_materialcomment_material'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='due_datetime',
            field=models.DateTimeField(null=True),
        ),
    ]