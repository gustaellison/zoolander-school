# Generated by Django 5.0.1 on 2024-01-22 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0029_assignmentsubmission'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='grade',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]