# Generated by Django 4.2.2 on 2023-06-23 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_customer_email_customer_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='nickname',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
