# Generated by Django 4.1.3 on 2023-08-21 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project2', '0012_alter_attendancerecord_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendancerecord',
            name='academic_year',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
    ]
