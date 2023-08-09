# Generated by Django 4.2.3 on 2023-08-09 08:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account_app', '0025_remove_student_subject_remove_student_teacher_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('contact_number', models.CharField(blank=True, max_length=10, null=True)),
                ('place', models.CharField(blank=True, max_length=50, null=True)),
                ('lesson_time', models.TimeField(blank=True, null=True)),
                ('more_information', models.TextField(blank=True, max_length=500, null=True)),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account_app.teacherssubject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('year', models.PositiveIntegerField()),
                ('place', models.CharField(blank=True, max_length=50, null=True)),
                ('lesson_time', models.TimeField(blank=True, null=True)),
                ('students', models.ManyToManyField(blank=True, related_name='groups', to='students_and_groups.student')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account_app.teacherssubject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]