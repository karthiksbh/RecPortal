# Generated by Django 3.2.8 on 2021-11-11 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_rename_user_results_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='reg_no',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
