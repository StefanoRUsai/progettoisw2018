# Generated by Django 2.0.6 on 2018-06-19 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookingApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='roomNumber',
            field=models.IntegerField(default=0),
        ),
    ]
