# Generated by Django 5.0.4 on 2024-05-15 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_slot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('slots_available', models.IntegerField(default=0)),
                ('slots_booked', models.IntegerField(default=0)),
                ('max_slots', models.IntegerField(default=10)),
            ],
        ),
        migrations.DeleteModel(
            name='HourReservation',
        ),
    ]
