# Generated by Django 4.2.2 on 2023-06-16 00:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slack_bridge', '0007_chatslack_message_id_info_chatslack_message_info_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatslack',
            name='message_info',
        ),
        migrations.AlterField(
            model_name='messageslackbridge',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 16, 3, 46, 2, 854232)),
        ),
    ]
