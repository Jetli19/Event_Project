# Generated by Django 4.1.1 on 2022-10-10 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_event_participants'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='end_event',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='start_event',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
