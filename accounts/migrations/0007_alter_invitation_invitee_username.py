# Generated by Django 4.2.9 on 2024-03-09 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_invitation_invitee_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='invitee_username',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
    ]
