# Generated by Django 3.0.5 on 2020-11-16 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dating', '0005_room_messages_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
    ]
