# Generated by Django 3.2.8 on 2021-11-24 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_rename_answer_text_answer_option'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='option',
            new_name='answer_text',
        ),
    ]