# Generated by Django 3.2.8 on 2021-11-22 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_alter_results_temp_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='results',
            name='temp_time',
            field=models.TimeField(default='0:00:00'),
        ),
    ]
