# Generated by Django 4.2.2 on 2023-07-15 01:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slack_bridge', '0009_alter_messageslackbridge_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messageslackbridge',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 15, 4, 48, 55, 370047)),
        ),
    ]
