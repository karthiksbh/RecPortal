# Generated by Django 3.2.8 on 2021-11-29 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0035_alter_questionstags_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionstags',
            name='tags',
            field=models.CharField(choices=[('Microcontroller and Microprocessors', 'Microcontroller and Microprocessors'), ('Digital logic design', 'Digital logic design'), ('Sensors', 'Sensors'), ('Basic electronics', 'Basic electronics'), ('IoT', 'IoT'), ('Python', 'Python'), ('DSA - Trees mostly', 'DSA - Trees mostly'), ('Competitive Coding', 'Competitive Coding'), ('CAO - basic computer knowledge stuff', 'CAO - basic computer knowledge stuff'), ('Logical reasoning ', 'Logical reasoning'), ('Exposure triangle', 'Composition'), ('Framing', 'Framing'), ('Editing', 'Editing'), ('Software', 'Software'), ('Hardware', 'Hardware'), ('UI/UX', 'UI/UX'), ('Vectors', 'Vectors'), ('Colour Palette', 'Colour Palette'), ('Figma', 'Figma'), ('Typography', 'Typography'), ('Teamwork', 'Teamwork'), ('Radical thinking', 'Radical thinking'), ('Convincing skills', 'Convincing skills'), ('Assertiveness', 'Assertiveness'), ('Communication skills', 'Communication skills'), ('Decisiveness', 'Decisiveness'), ('Empathy', 'Empathy'), ('Honesty/Trust', 'Honesty/Trust'), ('Vision and Communicating', 'Vision and Communicating'), ('Autonomous and Responsible', 'Autonomous and Responsible'), ('How to Be in Command', 'How to Be in Command')], max_length=100, verbose_name='Tags'),
        ),
    ]
