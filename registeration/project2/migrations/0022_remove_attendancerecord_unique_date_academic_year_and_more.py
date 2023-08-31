# Generated by Django 4.1.3 on 2023-08-31 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project2', '0021_attendancerecord_students_eftekad_notyet'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='attendancerecord',
            name='unique_date_academic_year',
        ),
        migrations.AddConstraint(
            model_name='attendancerecord',
            constraint=models.UniqueConstraint(fields=('date', 'academic_year', 'day_title'), name='unique_date_academic_year_day_title'),
        ),
    ]
