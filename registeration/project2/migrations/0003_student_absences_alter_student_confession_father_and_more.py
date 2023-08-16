# Generated by Django 4.1.3 on 2023-08-13 00:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project2', '0002_remove_student_brothers_student_brothers'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='absences',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='student',
            name='confession_father',
            field=models.CharField(blank=True, choices=[('لا يوجد', 'لا يوجد'), ('ابونا تاردس', 'ابونا تادرس'), ('ابونا سيرافيم', 'ابونا سيرافيم'), ('ابونا تيمثاوس', 'ابونا تيمثاوس'), ('اب كاهن اخر', 'اب كاهن اخر')], default='لا يوجد', max_length=15),
        ),
        migrations.AlterField(
            model_name='student',
            name='date_of_birth',
            field=models.DateField(blank=True, default=datetime.date(2000, 1, 1)),
        ),
        migrations.AlterField(
            model_name='student',
            name='facebook_profile',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='health_problems',
            field=models.TextField(blank=True, default='لا يوجد'),
        ),
        migrations.AlterField(
            model_name='student',
            name='hobbies',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='home_address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='home_region',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='home_town',
            field=models.TextField(blank=True, default='منوف'),
        ),
        migrations.AlterField(
            model_name='student',
            name='how_to_church',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='phone_number',
            field=models.CharField(blank=True, max_length=11),
        ),
        migrations.AlterField(
            model_name='student',
            name='phone_number2',
            field=models.CharField(blank=True, max_length=11),
        ),
        migrations.AlterField(
            model_name='student',
            name='school_name',
            field=models.TextField(blank=True),
        ),
    ]
