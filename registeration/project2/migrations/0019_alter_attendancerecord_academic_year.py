# Generated by Django 4.1.3 on 2023-08-27 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project2', '0018_alter_attendancerecord_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancerecord',
            name='academic_year',
            field=models.CharField(blank=True, choices=[('12', '12'), ('34', '34'), ('56', '56')], default='', max_length=30),
        ),
    ]
