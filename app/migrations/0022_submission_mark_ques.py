# Generated by Django 3.2.8 on 2021-11-22 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_auto_20211122_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='mark_ques',
            field=models.IntegerField(default=0),
        ),
    ]
