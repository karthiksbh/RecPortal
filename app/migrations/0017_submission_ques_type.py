# Generated by Django 3.2.8 on 2021-11-20 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_user_is_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='ques_type',
            field=models.IntegerField(choices=[(0, 'MCQ'), (1, 'LONG')], default=0, verbose_name='Question Type'),
        ),
    ]