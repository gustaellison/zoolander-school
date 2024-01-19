# Generated by Django 4.2.9 on 2024-01-19 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0015_alter_classroom_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='student',
        ),
        migrations.RemoveField(
            model_name='classroom',
            name='teacher',
        ),
        migrations.AddField(
            model_name='classroom',
            name='students',
            field=models.ManyToManyField(to='main_app.student'),
        ),
        migrations.AddField(
            model_name='classroom',
            name='teachers',
            field=models.ManyToManyField(to='main_app.teacher'),
        ),
    ]
