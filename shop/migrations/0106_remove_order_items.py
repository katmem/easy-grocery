# Generated by Django 2.0.7 on 2019-07-31 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0105_auto_20190731_1458'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
    ]