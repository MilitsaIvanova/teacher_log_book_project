# Generated by Django 4.2.3 on 2023-08-02 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('to_do_list_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
