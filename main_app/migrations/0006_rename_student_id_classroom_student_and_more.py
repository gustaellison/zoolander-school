# Generated by Django 5.0.1 on 2024-01-18 04:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_remove_student_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classroom',
            old_name='student_id',
            new_name='student',
        ),
        migrations.RenameField(
            model_name='classroom',
            old_name='teacher_id',
            new_name='teacher',
        ),
    ]