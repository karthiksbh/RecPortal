# Generated by Django 3.2.8 on 2021-11-22 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_alter_submission_mark_ques'),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='temp_time',
            field=models.TimeField(default='0:00:00'),
        ),
    ]
