# Generated by Django 3.2.8 on 2021-12-30 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0037_results_discrepancies'),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='result_checked',
            field=models.BooleanField(default=0),
        ),
    ]
