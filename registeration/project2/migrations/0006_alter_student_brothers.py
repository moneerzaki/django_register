# Generated by Django 4.1.3 on 2023-08-13 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project2', '0005_alter_student_absences_remove_student_brothers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='brothers',
            field=models.JSONField(default=list),
        ),
    ]
