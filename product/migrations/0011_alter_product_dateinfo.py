# Generated by Django 4.2 on 2023-05-10 22:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_month_plan_name_alter_product_dateinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='dateinfo',
            field=models.DateField(default=datetime.datetime(2023, 5, 10, 22, 59, 39, 464173)),
        ),
    ]
