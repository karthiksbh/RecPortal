# Generated by Django 3.2.8 on 2021-11-22 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_rename_user_submission_sub_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='is_checked',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='submission',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question', to='app.question'),
        ),
    ]
