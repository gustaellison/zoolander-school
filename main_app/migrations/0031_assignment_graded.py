# Generated by Django 5.0.1 on 2024-01-22 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0030_assignment_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='graded',
            field=models.BooleanField(default=False),
        ),
    ]
