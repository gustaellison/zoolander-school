# Generated by Django 5.0.1 on 2024-01-23 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0032_alter_student_classroom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='classroom',
            field=models.ManyToManyField(blank=True, related_name='classroom_relation', to='main_app.classroom'),
        ),
    ]