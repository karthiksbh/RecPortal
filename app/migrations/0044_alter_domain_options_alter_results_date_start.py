# Generated by Django 4.1 on 2022-09-04 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0043_alter_question_ques_main"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="domain",
            options={
                "ordering": ["id"],
                "verbose_name": "Domain",
                "verbose_name_plural": "Domains",
            },
        ),
        migrations.AlterField(
            model_name="results", name="date_start", field=models.DateField(),
        ),
    ]