# Generated by Django 4.1.2 on 2022-10-19 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0006_event_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(max_length=100, null=True),
        ),
    ]