# Generated by Django 3.2.8 on 2021-11-21 02:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_alter_submission_domain'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submission',
            old_name='user',
            new_name='sub_student',
        ),
    ]
