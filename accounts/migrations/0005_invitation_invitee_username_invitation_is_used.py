# Generated by Django 4.2.9 on 2024-03-09 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_invitation'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='invitee_username',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='invitation',
            name='is_used',
            field=models.BooleanField(default=False),
        ),
    ]