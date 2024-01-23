# Generated by Django 5.0.1 on 2024-01-22 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0023_classroom_zoom_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='submitted_by_student',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='assignment',
            name='submitted_file',
            field=models.FileField(blank=True, null=True, upload_to='assignment_submissions/'),
        ),
    ]
