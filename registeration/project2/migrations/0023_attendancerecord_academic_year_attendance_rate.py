# Generated by Django 4.1.3 on 2023-08-31 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project2', '0022_remove_attendancerecord_unique_date_academic_year_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendancerecord',
            name='academic_year_attendance_rate',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
