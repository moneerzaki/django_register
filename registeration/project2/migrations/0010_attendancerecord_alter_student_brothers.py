# Generated by Django 4.1.3 on 2023-08-20 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project2', '0009_student_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('day_title', models.CharField(default='مدارس احد', max_length=30)),
            ],
        ),
        migrations.AlterField(
            model_name='student',
            name='brothers',
            field=models.ManyToManyField(blank=True, default=list, to='project2.student'),
        ),
    ]
