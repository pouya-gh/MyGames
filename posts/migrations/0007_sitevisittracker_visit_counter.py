# Generated by Django 4.2.9 on 2024-04-08 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_sitevisittracker'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitevisittracker',
            name='visit_counter',
            field=models.IntegerField(default=1),
        ),
    ]
