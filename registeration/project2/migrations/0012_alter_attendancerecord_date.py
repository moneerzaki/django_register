# Generated by Django 4.1.3 on 2023-08-20 14:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project2', '0011_attendancerecord_students_present'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancerecord',
            name='date',
            field=models.DateField(default=datetime.datetime.today),
        ),
    ]